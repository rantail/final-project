from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

from .models import db, User, Word, Attempt
from .utils import normalize_text, clamp_level
from .dictionary import sample_words

def create_user(username: str, password: str) -> User:
    user = User(username=username.strip(), password_hash=generate_password_hash(password), level="Beginner")
    db.session.add(user)
    db.session.commit()
    return user

def verify_user(username: str, password: str) -> User | None:
    user = User.query.filter(func.lower(User.username) == username.strip().lower()).first()
    if not user:
        return None
    if not check_password_hash(user.password_hash, password):
        return None
    return user

def set_user_level(user: User, level: str):
    user.level = clamp_level(level)
    db.session.commit()

def add_word(user_id: int, prompt: str, answer: str, level: str = "Beginner") -> Word:
    w = Word(user_id=user_id, prompt=prompt.strip(), answer=answer.strip(), level=clamp_level(level))
    db.session.add(w)
    db.session.commit()
    return w

def import_random_words(user: User, k: int = 50, include_lower: bool = True) -> int:
    # avoid duplicates by prompt
    existing = {w.prompt.strip().lower() for w in Word.query.filter_by(user_id=user.id).all()}
    picked = sample_words(user.level, k=k, include_lower=include_lower)
    added = 0
    for it in picked:
        p = it["prompt"].strip()
        if p.lower() in existing:
            continue
        db.session.add(Word(user_id=user.id, prompt=p, answer=it["answer"].strip(), level=it.get("level","Beginner")))
        existing.add(p.lower())
        added += 1
    db.session.commit()
    return added

def check_answer(word: Word, user_input: str) -> bool:
    return normalize_text(user_input) == normalize_text(word.answer)

def record_attempt(user: User, word: Word, user_input: str, is_correct: bool) -> Attempt:
    now = datetime.utcnow()
    seconds_since_last = None
    if word.last_seen_at:
        seconds_since_last = int((now.replace(tzinfo=None) - word.last_seen_at.replace(tzinfo=None)).total_seconds())

    word.times_shown += 1
    if is_correct:
        word.times_correct += 1
        word.streak += 1
    else:
        word.streak = 0
    word.last_seen_at = now

    att = Attempt(
        user_id=user.id,
        word_id=word.id,
        user_input=user_input.strip(),
        is_correct=is_correct,
        seconds_since_last=seconds_since_last
    )
    db.session.add(att)
    db.session.commit()
    return att
