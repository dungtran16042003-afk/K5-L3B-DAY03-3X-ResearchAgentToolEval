"""summarize_text — tóm tắt rút trích (extractive) một đoạn văn tiếng Việt.

Tool local (không gọi mạng). Chấm điểm mỗi câu bằng tổng tần suất từ của câu
(bỏ stopword), rồi chọn tối đa max_sentences câu điểm cao nhất, giữ thứ tự gốc.

Nguyên tắc của lab: tool TRẢ ERROR DICT thay vì raise khi model gửi input xấu
(chuỗi rỗng, sai kiểu) để agent đọc được lỗi và hỏi lại user thay vì crash.
"""
from __future__ import annotations

import re

_WORD_RE = re.compile(r"\w+", re.UNICODE)
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?…])\s+")

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


def summarize_text(text: str, max_sentences: int = 3) -> dict:
    """Tóm tắt extractive: chọn các câu quan trọng nhất của đoạn văn.

    Returns:
        dict có summary/sentence_count/selected_count,
        hoặc dict {"error": ...} khi input không dùng được (không bao giờ raise).
    """
    if not isinstance(text, str):
        return {"error": f"text must be a string, got {type(text).__name__}: {text!r}"}
    if not isinstance(max_sentences, int) or isinstance(max_sentences, bool) or max_sentences < 1:
        return {"error": f"max_sentences must be an integer >= 1, got {max_sentences!r}"}
    if not text.strip():
        return {"error": "text must not be empty or whitespace-only"}

    sentences = [s.strip() for s in _SENT_SPLIT_RE.split(text) if s.strip()]

    word_freq: dict[str, int] = {}
    for word in _WORD_RE.findall(text.lower()):
        if word in _STOPWORDS or len(word) < 2 or word.isdigit():
            continue
        word_freq[word] = word_freq.get(word, 0) + 1

    def sentence_score(sentence: str) -> int:
        return sum(word_freq.get(w.lower(), 0) for w in _WORD_RE.findall(sentence))

    ranked = sorted(range(len(sentences)), key=lambda i: sentence_score(sentences[i]), reverse=True)
    chosen = sorted(ranked[:max_sentences])

    return {
        "summary": " ".join(sentences[i] for i in chosen),
        "sentence_count": len(sentences),
        "selected_count": len(chosen),
    }
