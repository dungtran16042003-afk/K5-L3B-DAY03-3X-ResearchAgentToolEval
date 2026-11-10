"""hashtag_suggester — đề xuất hashtag (không dấu, CamelCase) từ một đoạn text.

Tool local (không gọi mạng). Lấy các từ khóa hay gặp nhất (bỏ stopword, số),
bỏ dấu tiếng Việt rồi viết hoa chữ cái đầu, trả về tối đa max_tags hashtag.

Nguyên tắc của lab: tool TRẢ ERROR DICT thay vì raise khi model gửi input xấu
để agent đọc được lỗi và hỏi lại user thay vì crash.
"""
from __future__ import annotations

import re
import unicodedata

_WORD_RE = re.compile(r"\w+", re.UNICODE)

# "đ"/"Đ" không tách được bằng NFD nên phải map tay; các chữ có dấu khác thì
# normalize("NFD") + bỏ combining mark là hết dấu.
_DIACRITIC_MAP = str.maketrans({"đ": "d", "Đ": "D"})

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


def _strip_diacritics(word: str) -> str:
    decomposed = unicodedata.normalize("NFD", word.translate(_DIACRITIC_MAP))
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def hashtag_suggester(text: str, max_tags: int = 3) -> dict:
    """Đề xuất tối đa max_tags hashtag từ từ khóa chính của text.

    Returns:
        dict có hashtags/based_on,
        hoặc dict {"error": ...} khi input không dùng được (không bao giờ raise).
    """
    if not isinstance(text, str):
        return {"error": f"text must be a string, got {type(text).__name__}: {text!r}"}
    if not isinstance(max_tags, int) or isinstance(max_tags, bool) or max_tags < 1:
        return {"error": f"max_tags must be an integer >= 1, got {max_tags!r}"}
    if not text.strip():
        return {"error": "text must not be empty or whitespace-only"}

    freq: dict[str, int] = {}
    for word in _WORD_RE.findall(text.lower()):
        if word in _STOPWORDS or len(word) < 2 or word.isdigit():
            continue
        freq[word] = freq.get(word, 0) + 1

    top = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:max_tags]

    return {
        "hashtags": ["#" + _strip_diacritics(word).capitalize() for word, _ in top],
        "based_on": [word for word, _ in top],
    }
