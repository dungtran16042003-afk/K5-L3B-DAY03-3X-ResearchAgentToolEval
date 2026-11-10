---
name: keyword_extractor
track: core
kind: local_formatter
provider: none
requires_env: []
inputs: [text, top_k]
outputs: [keywords, counts, total_words]
side_effect: false
---

# keyword_extractor

Tool do nhóm tự viết cho CP3. Trích xuất `top_k` từ khóa hay gặp nhất trong
một đoạn văn tiếng Việt/Anh (bỏ stopword, số, từ 1 ký tự), kèm số lần xuất hiện.

## Khi nào dùng

- Cần biết chủ đề chính của một đoạn text đã có (bài fetch về, phản hồi, transcript).
- Chuẩn bị từ khóa cho `hashtag_suggester` hoặc tiêu đề cho `format`.

## Khi nào KHÔNG dùng

- Tìm bài đăng/theo dõi tài khoản → dùng `social_search` / `timeline`.
- Tóm tắt nội dung thành đoạn văn → dùng `summarize_text`.

## Ví dụ

Input:

```json
{"text": "AI và dữ liệu. AI học từ dữ liệu.", "top_k": 2}
```

Output:

```json
{"keywords": ["ai", "dữ"], "counts": {"ai": 2, "dữ": 2}, "total_words": 5}
```

## Ghi chú

- Tool thuần local: không gọi mạng, không cần env key.
- Tiếng Việt tách theo từ đơn ("dữ liệu" thành "dữ", "liệu") — đủ dùng để nhận diện chủ đề.
- Input xấu (chuỗi rỗng, `top_k` sai kiểu/giá trị) trả `{"error": ...}` thay vì raise.
