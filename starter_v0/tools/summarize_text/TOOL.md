---
name: summarize_text
track: core
kind: local_formatter
provider: none
requires_env: []
inputs: [text, max_sentences]
outputs: [summary, sentence_count, selected_count]
side_effect: false
---

# summarize_text

Tool do nhóm tự viết cho CP3. Tóm tắt rút trích (extractive) một đoạn văn
tiếng Việt: chấm điểm mỗi câu bằng tổng tần suất từ (đã bỏ stopword), chọn tối
đa `max_sentences` câu điểm cao nhất và giữ thứ tự gốc.

## Khi nào dùng

- Có văn bản dài (kết quả `fetch`, bài báo, phản hồi khách hàng) cần rút gọn
  trước khi trình bày digest cho user.
- Giảm số câu của nội dung đã có, giữ nguyên câu gốc (không bịa lời mới).

## Khi nào KHÔNG dùng

- Cần thông tin mới chưa có trong text → dùng `lookup` / `social_search`.
- Cần trích từ khóa/chủ đề chính → dùng `keyword_extractor`.

## Ví dụ

Input:

```json
{"text": "AI đang phát triển nhanh. Trời hôm nay đẹp. Nhiều công ty ứng dụng AI.", "max_sentences": 1}
```

Output:

```json
{"summary": "Nhiều công ty ứng dụng AI.", "sentence_count": 3, "selected_count": 1}
```

## Ghi chú

- Tool thuần local: không gọi mạng, không cần env key.
- Input xấu (chuỗi rỗng, `max_sentences` sai kiểu/giá trị) trả `{"error": ...}`
  thay vì raise (xem `tests/test_tools_todo.py`).
