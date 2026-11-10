# Báo cáo cá nhân — Lê Quốc Khánh

## 1. Thông tin thành viên

- Họ tên: Lê Quốc Khánh
- MSSV: 2A202603742
- Email: <!-- TODO: điền email của bạn -->

## 2. Phần việc phụ trách

- **CP3 — Tool mới và unit test**: viết 4 tool mới cho agent (đủ điều kiện bonus "Hơn 3 tool mới ≥ 4"), kèm unit test cho từng tool.
- Dọn lại bản nháp sai cấu trúc do AI khác (Copilot) tạo trước đó: file tool nằm sai vị trí (`tools/feedback_analyzer.py` thay vì `tools/feedback_analyzer/tool.py`), TOOL.md sai định dạng frontmatter, test nằm sai thư mục (`tests/starter_v0/tests/`).
- Phát hiện và xử lý **API key OpenAI thật bị dán vào `starter_v0/.env.example`** (file có trong repo) — đã revert file; key cần được thu hồi trên trang OpenAI.

## 3. Đóng góp cụ thể

- Viết 4 tool local (không gọi mạng, không cần API key), mỗi tool gồm `tool.py` + `TOOL.md` đúng contract trong `tools/README.md`:
  - `feedback_analyzer`: phân tích cảm xúc phản hồi tiếng Việt (positive/negative/neutral + điểm khen/chê), hiểu cả gõ có dấu và không dấu.
  - `summarize_text`: tóm tắt extractive — chọn các câu điểm cao nhất theo tần suất từ, giữ nguyên văn và thứ tự.
  - `keyword_extractor`: trích `top_k` từ khóa hay gặp kèm số lần xuất hiện (bỏ stopword/số, Việt + Anh).
  - `hashtag_suggester`: đề xuất hashtag không dấu CamelCase từ từ khóa chính ("đ" map tay sang "d" vì NFD không tách được).
- Đăng ký đủ 4 tool trong `tools/__init__.py` (`TOOL_FUNCTIONS`) và `artifacts/tools.yaml` (description ghi rõ *khi nào dùng / khi nào không dùng* theo chuẩn CP2).
- Áp dụng nguyên tắc lab: tool **trả error dict thay vì raise** khi model gửi input xấu (chuỗi rỗng, sai kiểu, số < 1) để agent đọc lỗi và hỏi lại user thay vì crash.
- Viết **13 unit test** (4 + 3 + 3 + 3) trong `tests/test_tools_todo.py`, mỗi tool có đủ: happy path, input xấu từ model, nhánh lỗi.
- Điền bảng **B5a** và dòng bonus "Hơn 3 tool mới (≥ 4)" trong `report/team/group_report.md`.

## 4. Bằng chứng

- File/commit/PR:
  - `starter_v0/tools/feedback_analyzer/{tool.py,TOOL.md}`
  - `starter_v0/tools/summarize_text/{tool.py,TOOL.md}`
  - `starter_v0/tools/keyword_extractor/{tool.py,TOOL.md}`
  - `starter_v0/tools/hashtag_suggester/{tool.py,TOOL.md}`
  - `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` (đăng ký tool)
  - `starter_v0/tests/test_tools_todo.py` (13 test mới)
  - `report/team/group_report.md` (B5a + bảng bonus)
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng AI assistant (ZCode) để viết code tool, TOOL.md, khai báo và unit test; trước đó một AI khác (Copilot) đã làm sai cấu trúc (tool sai vị trí, TOOL.md hỏng frontmatter, `raise` thay vì trả error dict, test sai thư mục) nên làm lại toàn bộ theo contract trong `tools/README.md`.
  - Tự kiểm tra bằng lệnh lab yêu cầu: `pytest` → **95 passed, 0 failed, 14 skipped** (skipped là stub challenge của tool có sẵn, được phép bỏ); `pytest tests/test_tool_contract.py` → **75 passed** (tools.yaml ↔ code ↔ TOOL.md đồng bộ sau khi thêm 4 tool).

## 5. Tự đánh giá

- Đã đạt yêu cầu CP3 (≥ 1 tool + ≥ 3 test) và vượt mức tối thiểu (4 tool, đủ điều kiện dòng bonus "≥ 4 tool mới" — còn phụ thuộc có eval case route tới tool mới trong CP4).
- Hiểu được sự khác nhau giữa **unit test** (đo code của tool: nhận args đó có chạy đúng không) và **eval** (đo lựa chọn của model: chọn tool/args có đúng không) — ví dụ model gọi `feedback_analyzer(feedback="tốt")` đúng args nhưng nếu code raise khi gặp input sai kiểu thì eval vẫn PASS mà agent vẫn crash; unit test là thứ bắt được lỗi đó.
- Điểm cần cải thiện: 4 tool đều thuần local (không gọi API ngoài) để chắc chắn chạy offline; chưa viết eval case route tới tool mới (thuộc CP4).
