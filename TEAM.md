# Team

## Thông tin nhóm

- Tên nhóm: 3X
- Lớp: L3B
- Repo nhóm: K5-L3B-3X-ResearchAgentToolEval
- URL repo, nhánh nộp, commit chốt: main (hoặc feat/prompt-eval tùy nhánh nộp của nhóm)

## Thành viên

| STT | Họ tên           | MSSV        | Email                       | GitHub               | Vai trò                                                                                                             |
| --: | ------------------ | ----------- | --------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------- |
|   1 | Nguyễn Tấn Dũng | 2A202603734 | 26ai.dungnt15@vinuni.edu.vn | dungtran16042003-afk | Leader / CP4, CP5 (Eval nhóm 10 case, Streamlit UI, Live chat, Group report Phần A & B3-B5) + Bonus Test challenge |
|   2 | Lê Huy Anh        | 2A202603786 | 26ai.anhlh5@vinuni.edu.vn   | hann1holic           | CP1, CP2 (Setup môi trường, Tối ưu Prompt & Tool v0–v4, Version log, Failure analysis B1-B2)                   |
|   3 | Lê Quốc Khánh   | 2A202603742 | 26ai.khanhlq2@vinuni.edu.vn | lqkhanhno            | CP3 (Phát triển 4 Tools mới local, Tool Contract, 13 Unit test, B5a) + 4 Tool                                    |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/team/` theo dạng: `report/team/MSSV_HoTen.md`.

---

## NguyenTanDung-2A202603734

### Phần việc phụ trách

- **CP4 — Eval nhóm:** Thiết kế và triển khai 10 test case vào `starter_v0/data/eval_group.json` (5 single-turn, 5 multi-turn), thực thi suite `--suite group`, phân tích và điền bảng B3 trong group report.
- **CP5 — UI, live chat, báo cáo:** Xây dựng giao diện Streamlit `starter_v0/app.py`, cấu hình `requirements.txt`, thực hiện phiên chat thực tế 5 lượt (`chat.py`) trích xuất transcript, hoàn thiện Phần A, B3, B4, B5a và các mục phản biện trong `report/team/group_report.md`.
- **Test challenge (Bonus):** Hoàn thiện 14 stub unit test cho 8 tool có sẵn trong `starter_v0/tests/test_tools_todo.py`.

### Đóng góp cụ thể

- Thiết kế bộ 10 eval case đo các khoảng trống của bộ base: boundary gửi tin (`send(confirmed=true)`), tham số mở rộng (`timeframe=month`, `max_results`), câu hỏi ngoài phạm vi dịch thuật, định tuyến tool nội bộ `format`, và định tuyến sang tool mới `summarize_text` (GM05).
- Chạy đánh giá suite group với OpenAI `gpt-4o-mini` trên artifact v4: run sạch `provider_error_cases == 0`, đạt 9 PASS / 1 FAIL (phân tích chi tiết lỗi case G05).
- Tái sử dụng vòng lặp model-tool của `chat.py` cho `app.py`, hỗ trợ hiển thị tool call trực quan và tự động lưu transcript phiên làm việc.
- Hoàn thành 14 unit test cho 8 tool mặc định, đưa toàn bộ test suite đạt **109 passed, 0 failed, 0 skipped**.
- Xử lý kỹ thuật: phát hiện và khắc phục lỗi hạn ngạch Gemini free-tier 429 Resource Exhausted bằng cách chuyển sang OpenAI `gpt-4o-mini`.

### Bằng chứng

- `starter_v0/data/eval_group.json`
- `starter_v0/runs/v4_B_group_openai_20261111T092953154103.json`
- `starter_v0/app.py` & `starter_v0/requirements.txt`
- `starter_v0/transcripts/v4_openai_20261110T190901045860.transcript.json`
- `starter_v0/tests/test_tools_todo.py` (14 test cho tool có sẵn)
- `report/team/group_report.md` (Phần A, B3, B4, B5a, B5 bonus)
- `report/team/2A202603734_NguyenTanDung.md`

---

## LeHuyAnh-2A202603786

### Phần việc phụ trách

- **CP1 — Setup và baseline v0:** Cấu hình môi trường (`.venv`, `requirements.txt`, `.env`), chạy preflight provider và đo lường baseline v0 trên bộ `eval_base.json`.
- **CP2 — Tối ưu prompt và tool declaration (v1–v4):** Thiết lập chu trình giả thuyết → chỉnh sửa → đo lường qua các phiên bản v1, v2, v3, v4 trên `artifacts/system_prompt.md` và `artifacts/tools.yaml`.
- Quản lý `artifacts/version_log.csv` và thực hiện phân tích lỗi các case FAIL cho Bảng B1, B2.

### Đóng góp cụ thể

- Chạy thành công baseline v0 trên model `gpt-4o-mini`, đạt accuracy gốc 65% (13/20 pass), xác định 7 case lỗi do chỉ dẫn xấu trong prompt ban đầu.
- Vòng lặp cải tiến v1 (85%): loại bỏ chỉ dẫn sai lệch, bổ sung nguyên tắc `clarify` khi thiếu dữ liệu và convention trích xuất tham số.
- Vòng lặp cải tiến v2 (95%): viết lại đặc tả `tools.yaml` chuẩn hóa tham số `response_type` và ranh giới an toàn cho `send`.
- Vòng lặp cải tiến v3 (95%): kiểm chứng và loại trừ giả thuyết bổ sung quy tắc văn bản thuần túy.
- Vòng lặp cải tiến v4 (100%): bổ sung few-shot demonstration cho luồng xác nhận đa lượt, đưa độ chính xác đạt tuyệt đối **20/20 pass (1.00 mọi metric)**.

### Bằng chứng

- `starter_v0/runs/v0_B_base_openai_20261110T173638837655.json` đến `v4_B_base_openai_20261110T180445506640.json`
- `starter_v0/artifacts/system_prompt.md` & `starter_v0/artifacts/tools.yaml`
- `starter_v0/artifacts/version_log.csv` (ghi nhận 5 phiên bản v0–v4)
- `report/team/group_report.md` (Bảng B1, B2)
- `report/team/2A202603786_LeHuyAnh.md`

---

## LeQuocKhanh-2A202603742

### Phần việc phụ trách

- **CP3 — Tool mới và unit test:** Xây dựng 4 công cụ mở rộng xử lý ngôn ngữ tiếng Việt chạy hoàn toàn local, đảm bảo tiêu chuẩn thiết kế tool an toàn.
- Chuẩn hóa cấu trúc thư mục, đồng bộ khai báo trong `tools/__init__.py` và `artifacts/tools.yaml`.
- Viết 13 unit test kiểm thử các nhánh logic của công cụ mới, hoàn thiện Bảng B5a trong group report.

### Đóng góp cụ thể

- Phát triển 4 công cụ local:
  - `feedback_analyzer`: phân tích cảm xúc phản hồi tiếng Việt có dấu và không dấu.
  - `summarize_text`: tóm tắt trích xuất (extractive summarization) theo tần suất từ vựng.
  - `keyword_extractor`: trích xuất `top_k` từ khóa đặc trưng loại bỏ từ dừng.
  - `hashtag_suggester`: sinh hashtag CamelCase không dấu chuẩn hóa.
- Thiết kế xử lý ngoại lệ theo nguyên tắc không làm gián đoạn hệ thống: trả về dictionary chứa thông báo lỗi thay vì phát sinh exception (`raise`) khi nhận dữ liệu không hợp lệ.
- Viết 13 unit test bao phủ trường hợp hoạt động chuẩn (happy path), dữ liệu sai kiểu và nhánh xử lý lỗi.
- Khắc phục cấu trúc thư mục và loại bỏ thông tin nhạy cảm (API key) khỏi các file cấu hình mẫu.

### Bằng chứng

- `starter_v0/tools/{feedback_analyzer,summarize_text,keyword_extractor,hashtag_suggester}/`
- `starter_v0/tools/__init__.py` & `starter_v0/artifacts/tools.yaml`
- `starter_v0/tests/test_tools_todo.py` (13 test mới cho 4 tool)
- `report/team/group_report.md` (Bảng B5a và mục Bonus công cụ mới)
- `report/team/2A202603742_LeQuocKhanh.md`
