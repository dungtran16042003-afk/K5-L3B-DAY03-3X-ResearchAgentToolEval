"""keyword_extractor — trích xuất từ khóa chính của một đoạn văn tiếng Việt/Anh.

Tool local (không gọi mạng). Đếm tần suất từ (bỏ stopword, số, từ 1 ký tự),
trả về top_k từ hay gặp nhất kèm số lần xuất hiện.

Nguyên tắc của lab: tool TRẢ ERROR DICT thay vì raise khi model gửi input xấu
để agent đọc được lỗi và hỏi lại user thay vì crash.
"""
from __future__ import annotations

import re

_WORD_RE = re.compile(r"\w+", re.UNICODE)

_STOPWORDS = {
    # Vietnamese
    "và", "hoặc", "nhưng", "vì", "nên", "với", "cho", "của", "các", "những",
    "một", "này", "đó", "kia", "khi", "rồi", "đã", "đang", "sẽ", "không",
    "có", "là", "được", "để", "trong", "trên", "dưới", "từ", "theo", "về",
    "bằng", "ra", "vào", "tôi", "bạn", "anh", "chị", "chúng", "nó", "họ",
    "rất", "cũng", "vừa", "nhiều", "ít", "hơn", "nhất", "nếu", "mà", "thì",
    "hay", "ở", "do", "tại", "như", "thế", "vậy",
    # English
    "the", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "this", "that", "it", "we",
    "you", "they", "he", "she", "at", "by", "as",
}


def keyword_extractor(text: str, top_k: int = 5) -> dict:
    """Trích xuất top_k từ khóa hay gặp nhất trong text.

    Returns:
        dict có keywords/counts/total_words,
        hoặc dict {"error": ...} khi input không dùng được (không bao giờ raise).
    """
    if not isinstance(text, str):
        return {"error": f"text must be a string, got {type(text).__name__}: {text!r}"}
    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        return {"error": f"top_k must be an integer >= 1, got {top_k!r}"}
    if not text.strip():
        return {"error": "text must not be empty or whitespace-only"}

    words = [
        w for w in _WORD_RE.findall(text.lower())
        if w not in _STOPWORDS and len(w) >= 2 and not w.isdigit()
    ]

    freq: dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    top = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:top_k]

    return {
        "keywords": [word for word, _ in top],
        "counts": dict(top),
        "total_words": len(words),
    }
