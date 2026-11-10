"""feedback_analyzer — phân tích cảm xúc phản hồi tiếng Việt của khách hàng.
 
Tool local (không gọi mạng, không cần API key). Nhận một đoạn phản hồi,
đếm các từ khóa khen/chê (có và không dấu) rồi trả về:
 
- sentiment: "positive" | "negative" | "neutral"
- positive_points / negative_points: các từ khóa tìm được
- word_count: độ dài phản hồi (số từ)
 
Nguyên tắc của lab: tool TRẢ ERROR DICT thay vì raise khi model gửi input xấu
(chuỗi rỗng, sai kiểu) để agent đọc được lỗi và hỏi lại user thay vì crash.
"""
from __future__ import annotations
 
# Mỗi từ khóa gồm dạng có dấu và không dấu (người Việt hay gõ cả hai).
_POSITIVE_KEYWORDS: list[tuple[str, str]] = [
    ("tốt", "tot"),
    ("nhanh", "nhanh"),
    ("hài lòng", "hai long"),
    ("tiện", "tien"),
    ("uy tín", "uy tin"),
    ("lịch sự", "lich su"),
    ("hiệu quả", "hieu qua"),
    ("tuyệt vời", "tuyet voi"),
]
 
_NEGATIVE_KEYWORDS: list[tuple[str, str]] = [
    ("tệ", "te"),
    ("chậm", "cham"),
    ("lâu", "lau"),
    ("khó chịu", "kho chiu"),
    ("đắt", "dat"),
    ("lỗi", "loi"),
    ("thất vọng", "that vong"),
    ("kém", "kem"),
]
 
 
def feedback_analyzer(feedback: str) -> dict:
    """Phân tích cảm xúc một đoạn phản hồi tiếng Việt.
 
    Returns:
        dict kết quả có sentiment/positive_points/negative_points/word_count,
        hoặc dict {"error": ...} khi input không dùng được (không bao giờ raise).
    """
    if not isinstance(feedback, str):
        return {
            "error": "feedback must be a string, got "
            f"{type(feedback).__name__}: {feedback!r}"
        }
    if not feedback.strip():
        return {"error": "feedback must not be empty or whitespace-only"}
 
    text = feedback.lower()
    positive_points = [label for label, alt in _POSITIVE_KEYWORDS if label in text or alt in text]
    negative_points = [label for label, alt in _NEGATIVE_KEYWORDS if label in text or alt in text]
 
    if len(positive_points) > len(negative_points):
        sentiment = "positive"
    elif len(positive_points) < len(negative_points):
        sentiment = "negative"
    else:
        sentiment = "neutral"
 
    return {
        "sentiment": sentiment,
        "positive_points": positive_points,
        "negative_points": negative_points,
        "word_count": len(feedback.split()),
    }
 