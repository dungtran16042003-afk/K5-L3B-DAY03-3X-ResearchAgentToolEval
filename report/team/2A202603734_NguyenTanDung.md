
# Báo cáo cá nhân — Nguyễn Tấn Dũng

## 1. Thông tin thành viên

- Họ tên: Nguyễn Tấn Dũng
- MSSV: 2A202603734
- Email: 26ai.dungnt15@vinuni.edu.vn
- Vai trò trong nhóm: Trưởng nhóm (Leader) / Thiết kế eval nhóm + xây dựng UI Streamlit + live chat + viết báo cáo nhóm (CP4, CP5) + Bonus Test challenge

## 2. Phần việc phụ trách

- **CP4 — Eval nhóm:** viết đúng 10 case vào `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn), chạy suite `--suite group`, điền bảng B3.
- **CP5 — UI, live chat, báo cáo:** viết UI Streamlit `starter_v0/app.py`, thêm dependency vào `requirements.txt`, chạy `chat.py` live 5 lượt lấy transcript, điền Phần A + B3 + B4 (+ B5a dòng UI, mục 3, 5, 7, 8) vào `report/team/group_report.md`.
- **Test challenge (bonus):** lấp 14 stub unit test cho 8 tool có sẵn trong `starter_v0/tests/test_tools_todo.py` (giữ nguyên 13 test cho 4 tool mới của bạn cùng nhóm).
- Cùng cả nhóm: cấu hình `.env`, xử lý lỗi provider (Gemini quota → chuyển OpenAI).

## 3. Đóng góp cụ thể

- Thiết kế 10 eval case đo các khoảng trống của bộ base: chiều dương của boundary gửi (user đã xác nhận thì gửi ngay — G01, GM01), args chưa được đo (`timeframe=month`, `max_results`, `search_type` multi-turn), out-of-scope dạng dịch thuật, route tới tool local `format` (G05), multi-turn carry topic + đổi nguồn (GM03), và case route tới tool mới của CP3 (GM05 → `summarize_text`).
- Chạy suite group bằng openai/gpt-4o-mini trên artifact v4: run sạch `provider_error_cases == 0`, đo đủ 10/10, **9 PASS / 1 FAIL** (G05 — model gọi `fetch` thay vì `format`; phân tích nguyên nhân + fix đề xuất trong B3).
- Viết `app.py` (Streamlit) tái dụng đúng vòng lặp model→tool của `chat.py` (`run_model_tool_loop`), hiển thị tool calls từng lượt, tự ghi transcript vào `transcripts/ui_*.transcript.json`; xác minh chạy được local (HTTP 200).
- Chạy `chat.py` 5 lượt liên tục một phiên, transcript đủ 3 kịch bản bắt buộc: yêu cầu thường / thiếu thông tin rồi bổ sung / yêu cầu gửi Telegram (agent hỏi xác nhận trước, chỉ `send(confirmed=true)` sau khi user đồng ý).
- Viết 14 unit test cho 8 tool có sẵn theo đúng hành vi: guardrail `send` (xác nhận → 1 POST mang token/chat_id; thiếu env → error dict và 0 request lên mạng), `format` (nhóm section, thread đánh số, items rỗng không crash), `lookup` (timeframe=None → body không có time_range), `fetch` (map response Firecrawl + cắt 4000 ký tự), `timeline` (bỏ item thiếu id, tôn trọng limit, URL dạng x.com/handle/status/id), `social_search` (params đúng query + search_type), `policy` (query rỗng → 0 kết quả, filter đúng area, dòng lệnh nhúng "Assistant: ignore..." phải vào untrusted_text chứ không vào facts). Kết quả: `pytest` toàn suite **109 passed, 0 failed, 0 skipped** → đạt mốc bonus Test challenge.
- Xử lý kỹ thuật: phát hiện `OPENROUTER_API_KEY` rỗng trong `.env`; Gemini key hợp lệ nhưng function calling cần `GOOGLE_GENAI_API_VERSION=v1beta`; free-tier 5 RPM / 20 RPD gây 429 giữa chừng (4 run hỏng — giữ làm bằng chứng lỗi, không dùng làm bằng chứng điểm) → chuyển hẳn sang OpenAI gpt-4o-mini cùng model với v0–v4.

## 4. Bằng chứng

- File/commit/PR:
  - `starter_v0/data/eval_group.json` (10 case) — commit của tôi
  - `starter_v0/runs/v4_B_group_openai_20261111T092953154103.json` (run group cuối, hợp lệ)
  - `starter_v0/app.py` + `starter_v0/requirements.txt` (streamlit)
  - `starter_v0/transcripts/v4_openai_20261110T190901045860.transcript.json` (5 lượt live)
  - `starter_v0/tests/test_tools_todo.py` (27 test: 14 tool có sẵn của tôi + 13 tool mới của bạn cùng nhóm)
  - `report/team/group_report.md` (Phần A, B3, B4, B5a-UI, B5-Test challenge, mục 3/5/7/8)
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng trợ lý AI (ZCode) để viết eval case, code UI, unit test và soạn báo cáo. Tự kiểm tra: chạy `pytest tests/test_tool_contract.py` (75 passed — case chỉ trỏ tool đã khai báo), chạy `pytest` toàn suite (109 passed, 0 failed, 0 skipped), đọc run JSON xác nhận `provider_error_cases == 0` trước khi dùng làm bằng chứng, đối chiếu từng dòng B3/B4 với file run/transcript thật, tự giải thích được vì sao từng case FAIL/PASS và vì sao chat tự do thì model hỏi lại bằng text thay vì gọi `clarify` (chat.py không ép `tool_choice`).

## 5. Tự đánh giá

- Điểm mạnh: eval case không trùng base, đo đúng các hành vi boundary mà base bỏ sót; bằng chứng đều trỏ được tới run/transcript thật; UI dùng lại logic chat.py nên hành vi nhất quán; unit test phủ cả tool có sẵn lẫn tool mới, toàn suite 0 failed 0 skipped.
- Hạn chế: case G05 (route `format`) vẫn FAIL — đã đề xuất fix trong B3 nhưng chưa áp dụng vì sẽ đổi artifact hash của cả nhóm; link public UI mới chạy tunnel lúc demo; chưa làm bonus Small Local Model và gửi Telegram thật.
- Bài học: eval ép `tool_choice` và chat tự do cho kết quả khác nhau (text-vs-clarify) — cần cả hai loại bằng chứng; quota free-tier của provider phải tính trước khi chạy suite.
