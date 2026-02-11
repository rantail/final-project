import json, random, os
from flask import current_app
from .utils import LEVELS, LEVEL_RANK, clamp_level

_cached = None

def load_global_dictionary():
    global _cached
    if _cached is not None:
        return _cached
    path = current_app.config.get("GLOBAL_WORDS_PATH")
    with open(path, "r", encoding="utf-8") as f:
        _cached = json.load(f)
    return _cached

def words_for_level(level: str, include_lower: bool = True):
    level = clamp_level(level)
    data = load_global_dictionary()
    if include_lower:
        max_rank = LEVEL_RANK[level]
        return [w for w in data if LEVEL_RANK.get(w.get("level","Beginner"),0) <= max_rank]
    return [w for w in data if w.get("level") == level]

def sample_words(level: str, k: int, include_lower: bool = True):
    pool = words_for_level(level, include_lower=include_lower)
    if not pool:
        return []
    k = max(1, min(int(k), len(pool)))
    return random.sample(pool, k)
