from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from .models import Word
from .services import add_word, check_answer, record_attempt, import_random_words, set_user_level
from .utils import clamp_level, LEVEL_RANK

api_bp = Blueprint("api", __name__)

@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})

@api_bp.post("/settings")
@login_required
def api_settings():
    data = request.get_json(silent=True) or {}
    level = clamp_level(data.get("level","Beginner"))
    set_user_level(current_user, level)
    return jsonify({"level": current_user.level})

@api_bp.post("/import")
@login_required
def api_import():
    data = request.get_json(silent=True) or {}
    k = int(data.get("k", 50))
    include_lower = bool(data.get("include_lower", True))
    added = import_random_words(current_user, k=k, include_lower=include_lower)
    return jsonify({"imported": added})

@api_bp.post("/words")
@login_required
def api_add_word():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    answer = (data.get("answer") or "").strip()
    level = clamp_level(data.get("level","Beginner"))
    if not prompt or not answer:
        return jsonify({"error": "prompt_and_answer_required"}), 400
    w = add_word(current_user.id, prompt, answer, level=level)
    return jsonify({"id": w.id, "prompt": w.prompt, "answer": w.answer, "level": w.level}), 201

@api_bp.post("/attempts")
@login_required
def api_attempt():
    data = request.get_json(silent=True) or {}
    word_id = data.get("word_id")
    user_input = (data.get("user_input") or "").strip()
    if not word_id or not user_input:
        return jsonify({"error": "word_id_and_user_input_required"}), 400

    w = Word.query.filter_by(id=int(word_id), user_id=current_user.id).first()
    if not w:
        return jsonify({"error": "word_not_found"}), 404

    is_correct = check_answer(w, user_input)
    record_attempt(current_user, w, user_input, is_correct)
    return jsonify({"correct": is_correct, "right_answer": w.answer})
