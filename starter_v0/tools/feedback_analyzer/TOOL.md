---
name: feedback_analyzer
track: core
kind: local_formatter
provider: none
requires_env: []
inputs: [feedback]
outputs: [sentiment, positive_points, negative_points, word_count]
side_effect: false
---

# feedback_analyzer

Tool do nhóm tự viết cho CP3. Phân tích cảm xúc một đoạn phản hồi tiếng Việt
của khách hàng bằng từ khóa (khen/chê, hỗ trợ cả gõ có dấu và không dấu).

## Khi nào dùng

- User đưa một đoạn text phản hồi/đánh giá và hỏi khách có hài lòng hay không.
- Tóm tắt điểm khen — điểm chê từ feedback đã thu thập được.

## Khi nào KHÔNG dùng

- Tìm bài đăng trên mạng xã hội → dùng `social_search`.
- Đọc nội dung một URL → dùng `fetch`.
- Chỉ dịch hoặc tóm tắt lại nội dung, không cần nhận định cảm xúc.

## Ví dụ

Input:

```json
{"feedback": "Dịch vụ rất tốt nhưng thời gian chờ lâu"}
```

Output:

```json
{
  "sentiment": "neutral",
  "positive_points": ["tốt"],
  "negative_points": ["lâu"],
  "word_count": 8
}
```

## Ghi chú

- Tool thuần local: không gọi mạng, không cần env key.
- Input xấu (chuỗi rỗng, sai kiểu) trả về `{"error": ...}` thay vì raise,
  để agent đọc lỗi và hỏi lại user (xem `tests/test_tools_todo.py`).
