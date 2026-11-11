# Báo cáo nhóm — Day 03 Research Agent Tool Eval

## 1. Thông tin nhóm

- Tên nhóm: 3X
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenAI `gpt-4o-mini` (CP1–CP2, runs `v0`–`v4`). Bộ eval nhóm (CP4), live chat và UI (CP5) cũng dùng OpenAI `gpt-4o-mini` trên cùng artifact (đã thử Gemini `gemini-2.5-flash` cho CP4/CP5 nhưng dính quota free-tier, xem mục 5)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent: tìm tin theo từ khóa trên web, bài đăng theo tài khoản, tweet theo chủ đề, đọc và tóm tắt URL, tìm paper arXiv, tra company policy nội bộ, tổng hợp thành digest markdown — và hỏi lại khi thiếu thông tin, xin xác nhận trước khi gửi gì đó lên Telegram.

**Cách chạy UI:**

```bash
cd starter_v0
streamlit run app.py     # dependency: streamlit đã thêm vào starter_v0/requirements.txt
```

**Link dùng thử (deploy):**

> Chạy `cloudflared tunnel --url http://localhost:8501` (hoặc cổng Streamlit đang chạy) rồi dán URL `https://<random>.trycloudflare.com` vào đây.
>
> URL: chưa deploy lên web, mới chỉ chạy localhost

### A2. Tool agent có

| Tên tool         | Làm được gì                                                                                    | Tool mới nhóm thêm? |
| ----------------- | --------------------------------------------------------------------------------------------------- | ---------------------- |
| clarify           | hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận yes/no trước hành động gửi | không                 |
| timeline          | lấy các bài đăng gần đây của một tài khoản (screenname không có @)                    | không                 |
| social_search     | tìm bài đăng theo từ khóa (search_type: Latest/Top)                                           | không                 |
| lookup            | tìm trên web (topic: general/news, timeframe: day/week/month/year)                                | không                 |
| fetch             | đọc nội dung một URL cụ thể                                                                   | không                 |
| format            | trình bày các item đã có thành markdown digest (brief/sections/bullets/thread)               | không                 |
| send              | gửi text lên Telegram, chỉ chạy khi user đã xác nhận (confirmed=true)                       | không                 |
| policy            | tra cứu company policy markdown nội bộ                                                           | không                 |
| papers            | tìm paper trên arXiv                                                                              | không                 |
| paper_text        | tải PDF arXiv và trích text cục bộ                                                             | không                 |
| feedback_analyzer | phân tích cảm xúc phản hồi tiếng Việt (positive/negative/neutral + điểm khen/chê)        | **có** (CP3)    |
| summarize_text    | tóm tắt extractive đoạn văn tiếng Việt thành N câu, giữ nguyên văn câu gốc            | **có** (CP3)    |
| keyword_extractor | trích top_k từ khóa kèm tần suất, bỏ stopword Việt/Anh                                      | **có** (CP3)    |
| hashtag_suggester | đề xuất hashtag không dấu CamelCase từ nội dung                                              | **có** (CP3)    |

### A3. Câu hỏi mẫu để thử

1. "Tin tức AI hôm nay có gì nổi bật?" — tra tin web theo ngày.
2. "Tóm tắt 5 tweet mới nhất giúp mình" — thiếu handle → agent phải hỏi lại thay vì đoán.
3. "Đăng bản tin này lên Telegram giúp mình" — agent phải xin xác nhận yes/no trước khi gọi send.
4. "Tìm paper arXiv về AI agent evaluation" — route tới tool papers.
5. "Theo company policy, tweet viral có được coi là fact đã xác nhận không?" — route tới tool policy.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **System prompt (CP2, v0→v4):** bỏ 3 chỉ dẫn xấu của starter; thêm rule clarify khi thiếu thông tin, out-of-scope không gọi tool, convention args (`lookup` query ngắn + `topic=news` + `timeframe`, `timeline` screenname không @); few-shot example cho luồng clarify(yes_no) → send(confirmed). Chi tiết từng version ở B1.
- **Tool declaration (CP2):** viết lại description `clarify` (LUÔN truyền `response_type`) và `send` (chỉ gọi khi `confirmed=true`, chưa xác nhận thì clarify yes_no).
- **Tool mới (CP3):** 4 tool local xử lý text tiếng Việt — `feedback_analyzer` (cảm xúc phản hồi), `summarize_text` (tóm tắt extractive), `keyword_extractor` (từ khóa + tần suất), `hashtag_suggester` (hashtag CamelCase) — mỗi tool trả error dict thay vì raise để agent hỏi lại user.
- **Eval nhóm (CP4):** 10 case đo các khoảng trống của base: chiều dương của boundary gửi (G01, GM01), timeframe=month, max_results, out-of-scope dịch thuật, route `format`, multi-turn sửa search_type / carry topic + đổi nguồn / huỷ tìm sang fetch, và route tới tool mới (GM05).
- **UI (CP5):** `app.py` Streamlit tái dụng vòng lặp tool của `chat.py`, ghi transcript cùng format.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact                                           | Hypothesis                                                                                                                                                     |                      Metric Before |                       Metric After | Run File                                             |
| ------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------: | ---------------------------------: | ---------------------------------------------------- |
| v0      | baseline                                                   | — (đo mốc, prompt xấu của starter dạy model đoán bừa / gửi không xác nhận / làm 1 bước)                                                        | case=0.65, routing=0.75, args=0.65 | case=0.65, routing=0.75, args=0.65 | `runs/v0_B_base_openai_20261110T173638837655.json` |
| v1      | `system_prompt.md` (prompt `eb1c8179` → `5edbb66d`) | Bỏ 3 chỉ dẫn xấu của starter, thêm rule: thiếu thông tin → `clarify`, out-of-scope → không gọi tool, convention args cho `lookup`/`timeline` | case=0.65, routing=0.75, args=0.65 | case=0.85, routing=0.95, args=0.85 | `runs/v1_B_base_openai_20261110T174447516616.json` |
| v2      | `tools.yaml` (tools `e69bc53e` → `9dbbe385`)        | Description `clarify`/`send` quá mơ hồ → viết lại: LUÔN truyền `response_type`; `send` chỉ gọi khi `confirmed=true`                        | case=0.85, routing=0.95, args=0.85 | case=0.95, routing=1.00, args=0.95 | `runs/v2_B_base_openai_20261110T175431755694.json` |
| v3      | `system_prompt.md` (prompt `5edbb66d` → `f39cb17e`) | Thêm rule tường minh "hành động gửi phải dùng `response_type='yes_no'`" — **không cải thiện**, loại trừ giả thuyết "thiếu rule"      | case=0.95, routing=1.00, args=0.95 | case=0.95, routing=1.00, args=0.95 | `runs/v3_B_base_openai_20261110T180056024580.json` |
| v4      | `system_prompt.md` (prompt `f39cb17e` → `0b5505a6`) | Rule bằng lời chưa đủ cho `gpt-4o-mini` → thêm few-shot example cụ thể cho luồng clarify(yes_no) → send(confirmed)                                | case=0.95, routing=1.00, args=0.95 | case=1.00, routing=1.00, args=1.00 | `runs/v4_B_base_openai_20261110T180445506640.json` |

Cả 5 run đều hợp lệ: `provider_error_cases == 0`, `measured_cases == total_cases == 20`. Provider: OpenAI (`gpt-4o-mini`). Chi tiết giả thuyết từng version: cột Hypothesis ở trên và `starter_v0/artifacts/version_log.csv`.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID                     | Failure Type    | Actual Tool Calls                                                                                                       | What Failed                                                                                                                                                                       | Fix                                                                              |
| --------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| R03_web_news_routing        | wrong_arg_value | `lookup(query="AI news", topic="news", timeframe="day")`                                                              | `query` phải là `"AI"` (từ "news" đã nằm trong `topic=news`)                                                                                                          | v1: thêm convention "query ngắn gọn" vào prompt                              |
| R08_out_of_scope            | out_of_scope    | `send(text="Nguyên hàm của x^2 là...")`                                                                           | Câu giải tích phân ngoài phạm vi → phải trả lời text, không gọi tool. Model còn dùng `send` làm công cụ trả lời                                              | v1: thêm rule out-of-scope "reply in text, call NO tool"                        |
| R10_missing_handle          | missing_info    | `timeline(screenname="sama")`                                                                                         | Không nói của ai → phải `clarify`, không được đoán theo gợi ý xấu "pick Sam Altman"                                                                               | v1: rule "NEVER guess"; v2: description `clarify` bắt buộc `response_type` |
| R11_missing_url             | missing_info    | `fetch(url="https://example.com/article")`                                                                            | "bài này" không có link → bịa URL thay vì hỏi                                                                                                                             | v1: rule "NEVER guess"; v2: như trên                                           |
| R12_confirm_before_send     | wrong_boundary  | v0: `send(text="Bản tin này")`; v2/v3: `clarify(response_type="text")`; v4: `clarify(response_type="yes_no")`  | Yêu cầu đăng lên Telegram phải được xác nhận yes/no trước khi `send`. Cần 3 lớp sửa: rule prompt (v1) + boundary trong description (v2) + few-shot example (v4) | v2 sửa `tools.yaml`, v4 thêm example                                         |
| R13_parallel_web_and_tweets | wrong_arg_value | `lookup(query="AI news")` (thiếu `topic=news`) + `social_search`                                                 | 2 nguồn nhưng args sai convention; làm 1 bước vội theo prompt xấu                                                                                                          | v1: convention + bỏ "single step"                                               |
| R14_out_of_scope_coding     | out_of_scope    | `send(text="def fibonacci...")`                                                                                       | Viết code Fibonacci ngoài phạm vi → không gọi tool                                                                                                                          | v1: rule out-of-scope                                                            |

Pattern chính: 7/7 FAIL của v0 đều bắt nguồn từ chỉ dẫn xấu có chủ đích trong prompt starter (đoán thay vì hỏi / gửi không cần xác nhận / luôn làm 1 bước) chứ không phải model "ngu". 6/7 hết sau v1–v2; R12 cần thêm v4 (few-shot). Case FAIL duy nhất còn lại ở v2–v3 (`R12`) được phân tích trung thực trong B1: v3 không tăng điểm nhưng loại trừ được giả thuyết "thiếu rule".

### B3. Team Eval Cases

Bộ đúng 10 case nhóm tự viết trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn), không trùng nội dung với `eval_base.json` / `eval_research_extension.json`. Run cuối: `starter_v0/runs/v4_B_group_openai_20261111T092953154103.json` (openai/gpt-4o-mini, artifact v4 + 4 tool mới của CP3, `provider_error_cases == 0`, đo đủ 10/10, **9 PASS / 1 FAIL**).

| Case ID                               | What It Tests                                                                                                                                                | Expected Tool/Behavior                                 | Result         |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ | -------------- |
| G01_send_after_explicit_confirmation  | User xác nhận gửi ngay trong lượt hỏi → gọi send luôn, không hỏi lại lần nữa                                                                   | `send(confirmed=true)`                               | PASS           |
| G02_lookup_timeframe_month            | "tháng này" → timeframe=month (base chỉ đo day/week)                                                                                                    | `lookup(topic=news, timeframe=month)`                | PASS           |
| G03_lookup_max_results                | Trích số lượng cho lookup: max_results=7                                                                                                                 | `lookup(query="climate change", max_results=7)`      | PASS           |
| G04_translation_out_of_scope          | Dịch thuật ngoài phạm vi research → không gọi tool nào                                                                                               | `no_tool`                                            | PASS           |
| G05_format_thread_routing             | Dữ liệu đã có sẵn trong lượt hỏi, chỉ cần trình bày → format local, không fetch                                                               | `format(template=thread)`                            | **FAIL** |
| GM01_confirm_then_send                | Multi-turn: lượt 1 xin gửi, lượt 2 xác nhận → send(confirmed=true), không hỏi lại lần 3                                                          | `send(confirmed=true)`                               | PASS           |
| GM02_search_type_correction           | Multi-turn: sửa search_type Top→Latest, giữ query "Llama 3"                                                                                               | `social_search(query="Llama 3", search_type=Latest)` | PASS           |
| GM03_carry_topic_switch_to_tweets     | Multi-turn: carry chủ đề "AI" + tự đổi nguồn web→social (không được chỉ đích danh)                                                            | `social_search(query="AI")`                          | PASS           |
| GM04_switch_lookup_to_fetch           | Multi-turn: huỷ tìm kiếm, trỏ thẳng URL → chỉ fetch, không lookup                                                                                    | `fetch(url=...anthropic.com/news/claude)`            | PASS           |
| GM05_route_to_summarize_text_new_tool | Multi-turn: đoạn văn có sẵn trong hội thoại + yêu cầu tóm tắt 2 câu → route tới TOOL MỚI `summarize_text` (CP3), không dùng lookup/format | `summarize_text(max_sentences=2)`                    | PASS           |

**Phân tích G05 (fail thật, xuất hiện nhất quán trên cả 2 provider):** khi user đưa kèm URL trong yêu cầu "đóng gói thành thread", model ưu tiên gọi `fetch` cho từng URL (3 extra calls) thay vì hiểu rằng dữ liệu title/url đã có sẵn và chỉ cần `format`. Nguyên nhân: system prompt v4 có rule routing cho lookup/timeline/clarify nhưng không có rule cho `format`, và description của `format` trong tools.yaml chưa nói "chỉ dùng khi dữ liệu đã có trong hội thoại, KHÔNG fetch thêm". Fix đề xuất (thuộc CP2 — chờ cả nhóm thống nhất vì sẽ đổi hash artifact): thêm 1 dòng routing rule cho `format` trong `system_prompt.md` hoặc viết lại description của `format`, sau đó chạy lại cả base + group suite với version mới.

### B4. Live Chat Evidence

Transcript: `starter_v0/transcripts/v4_openai_20261110T190901045860.transcript.json` (openai/gpt-4o-mini, artifact v4, 5 lượt liên tục một phiên).

| Turn | User Request                                                             | Tool Calls                                                         | Version Evidence               | Outcome                                                                                                                                                                                                              |
| ---- | ------------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | "Tin AI hôm nay có gì nổi bật?" (yêu cầu thường)                | `lookup(query="AI", topic="news", timeframe="day")`              | transcript turn 1, artifact v4 | Route + args đúng convention; backend Tavily trả lỗi kỹ thuật → agent báo lỗi thẳng, không bịa kết quả                                                                                                 |
| 2    | "Tóm tắt 5 tweet mới nhất giúp mình" (thiếu thông tin)           | không gọi tool nào — hỏi lại bằng text xin tên tài khoản | transcript turn 2              | KHÔNG đoán handle (đúng boundary); *ghi chú:* chat.py không ép `tool_choice` nên model hỏi bằng text thay vì gọi `clarify` (eval ép tool_choice đã chứng minh clarify routing ở G01/R10-R12) |
| 3    | "Của Elon Musk nhé" (bổ sung thông tin)                              | `timeline(screenname="elonmusk", limit=5)`                       | transcript turn 3              | Map tên→handle đúng, carry `limit=5` từ lượt 2; backend RapidAPI lỗi kỹ thuật → agent báo lỗi, không crash                                                                                           |
| 4    | "Đăng bản tin AI hôm nay lên Telegram giúp mình" (yêu cầu gửi) | không gọi `send` — hỏi xác nhận trước                    | transcript turn 4              | Đúng boundary: KHÔNG tự gửi, xin xác nhận yes/no trước (qua text, xem ghi chú turn 2)                                                                                                                      |
| 5    | "Có, mình xác nhận gửi"                                             | `send(confirmed=true)`                                           | transcript turn 5              | Sau xác nhận mới gọi send với `confirmed=true`; tool trả error dict vì chưa cấu hình `TELEGRAM_BOT_TOKEN/CHAT_ID` (bonus chưa làm) — agent báo lỗi thay vì crash                                 |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item                                 | Evidence File                                                                                                                 | What Worked                                                                                                                                                                                                                                                                     | Risk / Guardrail                                                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Tool mới `feedback_analyzer`      | `starter_v0/tools/feedback_analyzer/` (tool.py + TOOL.md), khai báo trong `tools/__init__.py` + `artifacts/tools.yaml` | Phân tích cảm xúc phản hồi tiếng Việt (positive/negative/neutral + điểm khen/chê), hiểu cả gõ có dấu/không dấu                                                                                                                                                | Input xấu (chuỗi rỗng, sai kiểu) trả error dict thay vì raise để agent hỏi lại user                            |
| Tool mới `summarize_text`         | `starter_v0/tools/summarize_text/`                                                                                          | Tóm tắt extractive tiếng Việt: chọn câu điểm cao nhất theo tần suất từ, giữ nguyên văn                                                                                                                                                                           | `max_sentences` sai kiểu/giá trị trả error dict                                                                    |
| Tool mới `keyword_extractor`      | `starter_v0/tools/keyword_extractor/`                                                                                       | Trích top_k từ khóa kèm counts, bỏ stopword/số (Việt + Anh)                                                                                                                                                                                                              | `top_k < 1` hoặc text sai kiểu trả error dict                                                                       |
| Tool mới `hashtag_suggester`      | `starter_v0/tools/hashtag_suggester/`                                                                                       | Đề xuất hashtag không dấu CamelCase ("đ" map tay vì NFD không tách được)                                                                                                                                                                                            | `max_tags` sai giá trị, text rỗng trả error dict                                                                   |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed)                                                                                                  | 27 test trong `starter_v0/tests/test_tools_todo.py` (14 cho 8 tool có sẵn + 13 cho 4 tool mới: happy path, input xấu từ model, nhánh lỗi); full suite **109 passed, 0 failed, 0 skipped**                                                                        | Toàn bộ test offline (mock HTTP bằng `fake_http`), không tốn credit API                                           |
| UI (lệnh chạy + link dùng thử)   | `starter_v0/app.py`, dependency `streamlit>=1.30.0` trong `starter_v0/requirements.txt`                                 | Streamlit chat UI tái dụng đúng vòng lặp model→tool của `chat.py` (import `run_model_tool_loop`), hiển thị tool calls từng lượt, tự ghi transcript vào `transcripts/ui_*.transcript.json`; đã chạy xác minh local `http://localhost:8501` (HTTP 200) | Link public cần `cloudflared tunnel --url http://localhost:8501` khi demo; tunnel chỉ sống trong phiên cloudflared |

Tool unit tests: 27 test đã viết. Ví dụ lỗi unit test bắt được mà eval không bắt được: nếu model gửi `feedback=123` (sai kiểu) thì bản code đầu tiên `raise ValueError` làm agent crash giữa lượt; eval chỉ chấm model *chọn* tool và *truyền* args có đúng không nên không phát hiện được — test `test_feedback_gui_so_thi_tra_error` bắt đúng nhánh này và buộc tool trả `{"error": ...}` để agent hỏi lại user. Ví dụ với tool có sẵn: `test_send_confirmed_without_env_returns_error_and_no_request` xác nhận `send` khi thiếu token phải trả error dict và **không phát request nào** lên mạng.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus                                            | Evidence File                                                                                                                             | What Worked                                                                                                                                                           | Risk / Guardrail                                                                                                                  |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Small Local Model                                | xem B7                                                                                                                                    |                                                                                                                                                                       |                                                                                                                                   |
| Hơn 3 tool mới (≥ 4)                          | `starter_v0/tools/{feedback_analyzer,summarize_text,keyword_extractor,hashtag_suggester}/` + 27 test trong `tests/test_tools_todo.py` | 4 tool local tự viết, mỗi tool đủ TOOL.md + đăng ký (`tools/__init__.py`, `artifacts/tools.yaml`) + ≥ 3 test; `pytest` 109 passed, 0 failed, 0 skipped | Có eval case route tới tool mới: `GM05_route_to_summarize_text_new_tool` trong `data/eval_group.json` — PASS trong run B3 |
| `send` gửi thật lên Telegram sau xác nhận | transcript                                                                                                                                |                                                                                                                                                                       |                                                                                                                                   |
| Test challenge (0 skipped / regression test)     | `pytest` output: **109 passed, 0 failed, 0 skipped** toàn suite                                                                  | Đã lấp hết 14 stub trong `tests/test_tools_todo.py` (clarify, format, send, lookup, fetch, timeline, social_search, policy) — đạt mốc 0 skipped của bonus  |                                                                                                                                   |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version            | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
| ------------------ | ---------------- | ------------ | ------------- | ------------ | -------- | --------- | -------- |
| v3                 | (cloud)          | v3           |               |              |          |           |          |
| v3-<model></model> | (ollama)         | v3           |               |              |          |           |          |
| v3-<model></model> | (ollama)         | v3           |               |              |          |           |          |
| v4-local           |                  |              |               |              |          |           |          |
| v5-local           |                  |              |               |              |          |           |          |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern                                 | Count | Example Case | Fix Tried | Helped? |
| ----------------------------------------------- | ----- | ------------ | --------- | ------- |
| wrong / hallucinated tool                       |       |              |           |         |
| invalid JSON args (`_invalid_json_arguments`) |       |              |           |         |
| no tool call / answered directly                |       |              |           |         |
| missed `clarify`                              |       |              |           |         |
| repeated / unnecessary calls                    |       |              |           |         |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

- **Hết quota Gemini free-tier khi chạy CP4:** định chạy suite group bằng `gemini-2.5-flash` nhưng free-tier giới hạn 5 request/phút và 20 request/ngày/model — 3 lần chạy đều dính 429 RESOURCE_EXHAUSTED (bằng chứng: 4 run JSON `runs/v4_B_group_gemini_2026111*.json` có `provider_error_cases > 0`, không dùng làm bằng chứng). Xử lý: đổi sang OpenAI `gpt-4o-mini` (key do bạn cùng nhóm cung cấp) — cùng model với v0–v4 nên kết quả so sánh được.
- **SDK google-genai gọi API v1 (không hỗ trợ function calling):** preflight Gemini báo 400 "Function calling is not enabled for api version v1". Xử lý không cần sửa code provider: set `GOOGLE_GENAI_API_VERSION=v1beta` trong `.env`.
- **Backend tool lỗi kỹ thuật trong live chat (turn 1, 3):** `lookup`/`timeline` gọi API thật (Tavily/RapidAPI) trả lỗi → agent báo lỗi thẳng cho user thay vì bịa kết quả (boundary đúng); xem `transcripts/v4_openai_20261110T190901045860.transcript.json`.
- **`send` chưa gửi được thật:** thiếu `TELEGRAM_BOT_TOKEN/CHAT_ID` trong `.env` — tool trả error dict, agent báo lỗi, không crash. Bonus Telegram chưa claim.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`? — v1 (bỏ chỉ dẫn xấu, thêm rule clarify/out-of-scope/convention), v3 (rule yes_no), v4 (few-shot example). Fix đề xuất cho G05 cũng thuộc prompt: thêm rule "dữ liệu đã có trong hội thoại → format, KHÔNG fetch lại".
- Fix nào thuộc `tools.yaml`? — v2 (description `clarify`/`send` + boundary confirmed). G05 cũng sửa được ở description `format` ("chỉ dùng khi item đã có, không dùng để đọc URL").
- Failure nào cần review thủ công thay vì chấm tự động? — chất lượng câu trả lời tổng hợp (digest có đúng nội dung tool trả về không), câu hỏi clarify có dễ hiểu không, và các lượt chat tự do không ép `tool_choice` (transcript cho thấy model hỏi lại bằng text thay vì gọi clarify — chấm tự động theo tool_calls sẽ đánh FAIL dù hành vi đúng).
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào? — v5: thêm rule routing cho `format` (chỉ G05 còn FAIL) rồi chạy lại cả base + group để xác nhận không tụt metric nào khác.

## 8. Tài liệu tham khảo

- Tài liệu lab: `README.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `starter_v0/README.md`, `starter_v0/tools/README.md`.
- OpenAI Chat Completions API (tool calling): https://platform.openai.com/docs/guides/function-calling
- Streamlit (chat UI): https://docs.streamlit.io/
- Google Gen AI SDK (đã thử cho CP4/CP5 trước khi chuyển sang OpenAI): https://googleapis.github.io/python-genai/
- Cloudflare Tunnel (expose UI khi demo): https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
