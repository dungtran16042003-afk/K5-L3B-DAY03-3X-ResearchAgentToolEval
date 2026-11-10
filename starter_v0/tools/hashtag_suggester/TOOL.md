---
name: hashtag_suggester
track: core
kind: local_formatter
provider: none
requires_env: []
inputs: [text, max_tags]
outputs: [hashtags, based_on]
side_effect: false
---

# hashtag_suggester

Tool do nhóm tự viết cho CP3. Đề xuất tối đa `max_tags` hashtag từ các từ khóa
hay gặp nhất của đoạn text: bỏ dấu tiếng Việt, viết hoa chữ cái đầu
(ví dụ "dữ liệu" → `#Du`, `#Lieu`).

## Khi nào dùng

- Chuẩn bị đăng digest/bài đăng lên mạng xã hội (thường gọi trước `send`).
- User hỏi "đăng kèm hashtag nào".

## Khi nào KHÔNG dùng

- Phân tích cảm xúc khách hàng → dùng `feedback_analyzer`.
- Tạo nội dung mới hoặc tìm nội dung → dùng `lookup` / `summarize_text`.

## Ví dụ

Input:

```json
{"text": "Trí tuệ nhân tạo và dữ liệu lớn", "max_tags": 3}
```

Output:

```json
{"hashtags": ["#Du", "#Lieu", "#Lon"], "based_on": ["dữ", "liệu", "lớn"]}
```

## Ghi chú

- Tool thuần local: không gọi mạng, không cần env key.
- "đ" được map tay sang "d" vì NFD không tách được chữ này.
- Input xấu (chuỗi rỗng, `max_tags` sai kiểu/giá trị) trả `{"error": ...}` thay vì raise.
