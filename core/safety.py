from core.refusal import Refusal

FORBIDDEN_WORDS = {
    "legal", "illegal", "allowed", "permitted",
    "valid", "compliant", "should", "can", "cannot"
}

def enforce_required_fields(data: dict, required_fields: list):
    for field in required_fields:
        if field not in data:
            raise Refusal(f"MISSING_REQUIRED_FIELD: {field}")

def enforce_no_unknown_fields(data: dict, allowed_fields: list):
    for key in data.keys():
        if key not in allowed_fields:
            raise Refusal(f"UNKNOWN_FIELD: {key}")

def enforce_forbidden_words(text: str):
    lowered = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in lowered:
            raise Refusal(f"FORBIDDEN_WORD_DETECTED: {word}")
