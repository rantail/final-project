import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from datetime import datetime

from .models import Attempt, Word
from .utils import LEVEL_RANK

def train_model_for_user(user_id: int):
    atts = Attempt.query.filter_by(user_id=user_id).all()
    if len(atts) < 30:
        return None

    rows = []
    for a in atts:
        w = Word.query.get(a.word_id)
        if not w:
            continue
        acc = (w.times_correct / w.times_shown) if w.times_shown else 0.0
        rows.append({
            "seconds_since_last": a.seconds_since_last if a.seconds_since_last is not None else np.nan,
            "streak": w.streak,
            "times_shown": w.times_shown,
            "accuracy_so_far": acc,
            "is_correct": 1 if a.is_correct else 0
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return None

    df["seconds_since_last"] = df["seconds_since_last"].fillna(df["seconds_since_last"].median())
    X = df[["seconds_since_last", "streak", "times_shown", "accuracy_so_far"]].to_numpy(dtype=float)
    y = df["is_correct"].to_numpy(dtype=int)

    if len(np.unique(y)) < 2:
        return None

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)
    return model

def predict_correct_probability(model, word: Word, seconds_since_last: int | None):
    acc = (word.times_correct / word.times_shown) if word.times_shown else 0.0
    if seconds_since_last is None:
        seconds_since_last = 3600

    if model is None:
        penalty = min(0.6, np.log1p(seconds_since_last) / 20.0)
        base = 0.2 + 0.7 * acc
        return float(max(0.05, min(0.95, base - penalty)))

    X = np.array([[float(seconds_since_last), float(word.streak), float(word.times_shown), float(acc)]], dtype=float)
    return float(model.predict_proba(X)[0][1])

def pick_next_word(user_id: int, max_level_rank: int):
    words = Word.query.filter_by(user_id=user_id).all()
    if not words:
        return None

    # filter words by level (<= user level)
    eligible = [w for w in words if LEVEL_RANK.get(w.level,0) <= max_level_rank]
    if not eligible:
        eligible = words

    model = train_model_for_user(user_id)
    now = datetime.utcnow()

    scored = []
    for w in eligible:
        seconds = None
        if w.last_seen_at:
            seconds = int((now.replace(tzinfo=None) - w.last_seen_at.replace(tzinfo=None)).total_seconds())
        p = predict_correct_probability(model, w, seconds)
        scored.append((p, w))

    scored.sort(key=lambda x: x[0])
    return scored[0][1]
