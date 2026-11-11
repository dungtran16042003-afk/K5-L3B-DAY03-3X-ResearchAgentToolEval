"""Streamlit UI cho Research Agent (CP5).

Chạy từ starter_v0/:
    streamlit run app.py

Dùng lại đúng vòng lặp model -> tool của chat.py nên hành vi giống hệt live chat.
Mỗi lượt chat được ghi thêm vào transcripts/ui_<provider>_<timestamp>.transcript.json.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import run_model_tool_loop, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"

load_lab_env(ROOT)

st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="centered")

# ---------- Sidebar: cấu hình ----------
with st.sidebar:
    st.header("⚙️ Cấu hình")
    provider_name = st.selectbox("Provider", ["gemini", "openrouter", "openai", "anthropic"], index=0)
    version_label = st.text_input("Version label", value="v4")
    max_tool_rounds = st.slider("Max tool rounds", 1, 6, 4)
    if st.button("🗑️ Xoá hội thoại"):
        st.session_state.clear()
        st.rerun()

# ---------- Init state ----------
if "history" not in st.session_state:
    st.session_state.history = []
if "transcript" not in st.session_state:
    system_prompt_text = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    artifact_version = build_artifact_version(version_label, ARTIFACTS_DIR / "system_prompt.md", ARTIFACTS_DIR / "tools.yaml")
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"ui_{provider_name}_{timestamp}"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "source": "streamlit_ui",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "turns": [],
    }
    st.session_state.turn_index = 0
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"

# Provider/tools nạp theo lựa chọn hiện tại
system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
openai_tools = to_openai_tools(load_tool_declarations(ARTIFACTS_DIR / "tools.yaml"))

try:
    provider = make_provider(provider_name)
    default_model = getattr(provider, "default_model", None)
except Exception as exc:  # thiếu key, thiếu SDK...
    st.error(f"Không khởi tạo được provider `{provider_name}`: {exc}")
    st.stop()

st.session_state.transcript["provider"] = provider_name

# ---------- Header ----------
st.title("🔎 Research Agent")
st.caption(
    f"Provider: **{provider_name}** · model: **{default_model}** · version: **{version_label}** — "
    "agent research tin tức / social / web / paper, hỏi lại khi thiếu info, xin xác nhận trước khi gửi."
)

# ---------- Render lịch sử ----------
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("tool_events"):
            with st.expander("🔧 Tool calls"):
                for event in msg["tool_events"]:
                    st.markdown(f"**`{event['tool']}`**")
                    st.json(event, expanded=False)

# ---------- Input ----------
user_text = st.chat_input("Nhập yêu cầu research của bạn…")
if user_text:
    st.session_state.history.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    st.session_state.turn_index += 1
    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    with st.chat_message("assistant"):
        with st.spinner("Agent đang nghĩ…"):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.history[-10:-1],
                        {"role": "user", "content": user_text},
                    ],
                    tools=openai_tools,
                    model=None,
                    max_tool_rounds=max_tool_rounds,
                )
            except Exception as exc:
                result = {
                    "status": "provider_error",
                    "assistant_text": f"⚠️ Lỗi provider: `{exc}`",
                    "rounds": [],
                    "tool_events": [],
                }

    assistant_text = result["assistant_text"]
    tool_events = result.get("tool_events", [])
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
        if tool_events:
            with st.expander("🔧 Tool calls"):
                for event in tool_events:
                    st.markdown(f"**`{event['tool']}`**")
                    st.json(event, expanded=False)

    turn_record.update({
        "status": result["status"],
        "assistant_text": assistant_text,
        "rounds": result.get("rounds", []),
        "tool_events": tool_events,
        "ended_at": datetime.now().isoformat(timespec="seconds"),
    })
    st.session_state.transcript["turns"].append(turn_record)
    st.session_state.transcript["updated_at"] = datetime.now().isoformat(timespec="seconds")
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)

    st.session_state.history.append({
        "role": "assistant",
        "content": assistant_text,
        "tool_events": tool_events,
    })
    st.rerun()

# ---------- Footer: gợi ý thử ----------
with st.expander("💡 Câu hỏi mẫu để thử"):
    st.markdown(
        "- Tin AI hôm nay có gì nổi bật?\n"
        "- Tóm tắt 5 tweet mới nhất giúp mình *(thiếu handle → agent phải hỏi lại)*\n"
        "- Đăng bản tin này lên Telegram giúp mình *(agent phải xin xác nhận trước khi gửi)*\n"
        "- Tìm paper arXiv về AI agent evaluation\n"
        "- Theo company policy, tweet viral có được coi là fact đã xác nhận không?"
    )
