import re

LEVELS = ["Beginner","A1","A2","B1","B2"]
LEVEL_RANK = {lvl:i for i,lvl in enumerate(LEVELS)}

def normalize_text(s: str) -> str:
    return (s or "").strip().lower()

def validate_username(username: str):
    username = (username or "").strip()
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3–20 characters."
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can contain only letters, digits, underscore."
    return True, ""

def validate_password(password: str):
    password = password or ""
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    return True, ""

def clamp_level(level: str) -> str:
    return level if level in LEVELS else "Beginner"
