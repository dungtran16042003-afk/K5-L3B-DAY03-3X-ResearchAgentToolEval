"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------- Tool mới của nhóm làm ở CP3 ----------
# 4 tool: feedback_analyzer, summarize_text, keyword_extractor, hashtag_suggester
# Với mỗi tool nhóm test 3 thứ:
# - happy path: input bình thường thì trả kết quả đúng
# - model gửi input rác (chuỗi rỗng, sai kiểu, số âm...) -> phải trả {"error": ...}
# - tool không được raise ra ngoài, để agent đọc được lỗi rồi hỏi lại user

# ---------------- feedback_analyzer ----------------

def test_feedback_binh_luan_khen_thi_positive() -> None:
    # Bình luận toàn lời khen -> sentiment = positive, không có điểm chê nào
    result = TOOL_FUNCTIONS["feedback_analyzer"](feedback="Giao hàng nhanh, đóng gói cẩn thận, chất lượng tốt")
    assert result["sentiment"] == "positive"
    assert "tốt" in result["positive_points"]
    assert "nhanh" in result["positive_points"]
    assert result["negative_points"] == []


def test_feedback_chue_nhieu_hon_khen_thi_negative() -> None:
    # Lời chê nhiều hơn lời khen -> sentiment = negative
    result = TOOL_FUNCTIONS["feedback_analyzer"](feedback="Ship chậm, app hay bị lỗi, hơi thất vọng")
    assert result["sentiment"] == "negative"
    assert "chậm" in result["negative_points"]
    assert "lỗi" in result["negative_points"]
    assert result["positive_points"] == []


def test_feedback_de_trong_thi_tra_error() -> None:
    # Có lúc user chỉ gõ dấu cách rồi gửi -> model sẽ truyền chuỗi rỗng vào tool
    # lúc này tool phải trả error dict chứ không raise làm crash agent
    result = TOOL_FUNCTIONS["feedback_analyzer"](feedback="   ")
    assert "error" in result
    assert "sentiment" not in result


def test_feedback_gui_so_thi_tra_error() -> None:
    # Model thi thoảng truyền sai kiểu (số thay vì chuỗi) -> cũng phải trả error dict
    result = TOOL_FUNCTIONS["feedback_analyzer"](feedback=12345)
    assert "error" in result
    assert "sentiment" not in result


# ---------------- summarize_text ----------------

def test_tom_tat_giu_lai_cau_chua_tu_khoa_chinh() -> None:
    # Câu lặp từ "tệ" nhiều lần là câu quan trọng nhất nên phải được giữ lại,
    # còn những câu lạc đề (đi chợ, chó con) phải bị loại
    text = (
        "Sản phẩm này dùng rất tệ. "
        "Hôm qua mình đi chợ mua rau. "
        "Tệ lắm, tệ thật, không đáng tiền. "
        "Chó con trông dễ thương quá."
    )
    result = TOOL_FUNCTIONS["summarize_text"](text=text, max_sentences=1)
    assert result["sentence_count"] == 4
    assert result["selected_count"] == 1
    assert "tệ" in result["summary"].lower()
    assert "chợ" not in result["summary"].lower()


def test_tom_tat_chuoi_rong_tra_error() -> None:
    result = TOOL_FUNCTIONS["summarize_text"](text="")
    assert "error" in result


def test_tom_tat_so_cau_sai_kieu_tra_error() -> None:
    # Model gửi max_sentences dạng chuỗi "3" thay vì số -> error, không crash
    result = TOOL_FUNCTIONS["summarize_text"](text="Một câu duy nhất.", max_sentences="3")
    assert "error" in result
    assert "max_sentences" in result["error"]


# ---------------- keyword_extractor ----------------

def test_keyword_tu_xuat_hien_nhieu_nhat_dung_dau() -> None:
    # "AI" lặp 3 lần nên phải đứng đầu danh sách, và chỉ trả đúng 2 từ vì top_k=2
    result = TOOL_FUNCTIONS["keyword_extractor"](
        text="AI đang thay đổi nhiều ngành. Các công ty AI tăng đầu tư. Học AI từ cơ bản.", top_k=2
    )
    assert result["keywords"][0] == "ai"
    assert result["counts"]["ai"] == 3
    assert len(result["keywords"]) == 2


def test_keyword_top_k_bang_0_tra_error() -> None:
    # top_k=0 là kiểu input rác model hay gửi -> error dict
    result = TOOL_FUNCTIONS["keyword_extractor"](text="AI đang phát triển", top_k=0)
    assert "error" in result
    assert "keywords" not in result


def test_keyword_text_none_tra_error() -> None:
    result = TOOL_FUNCTIONS["keyword_extractor"](text=None)
    assert "error" in result


# ---------------- hashtag_suggester ----------------

def test_hashtag_bo_dau_va_viet_hoa() -> None:
    # "dữ liệu lớn" phải được bỏ dấu rồi viết hoa thành hashtag: #Du #Lieu #Lon
    result = TOOL_FUNCTIONS["hashtag_suggester"](text="Trí tuệ nhân tạo và dữ liệu lớn", max_tags=3)
    assert result["hashtags"] == ["#Du", "#Lieu", "#Lon"]


def test_hashtag_text_rong_tra_error() -> None:
    result = TOOL_FUNCTIONS["hashtag_suggester"](text="   ")
    assert "error" in result
    assert "hashtags" not in result


def test_hashtag_max_tags_am_tra_error() -> None:
    # max_tags âm là input rác từ model -> error dict
    result = TOOL_FUNCTIONS["hashtag_suggester"](text="AI và dữ liệu", max_tags=-1)
    assert "error" in result
