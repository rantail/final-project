from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user

from .models import User, Word, Attempt
from .utils import validate_username, validate_password, LEVELS, LEVEL_RANK, clamp_level
from .services import create_user, verify_user, add_word, check_answer, record_attempt, import_random_words, set_user_level
from .ml import pick_next_word
from .stats import generate_charts_for_user

web_bp = Blueprint("web", __name__)

@web_bp.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("web.dashboard"))
    return redirect(url_for("web.login"))

@web_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        ok_u, msg_u = validate_username(username)
        ok_p, msg_p = validate_password(password)

        if not ok_u:
            flash(msg_u, "error"); return render_template("register.html", levels=LEVELS)
        if not ok_p:
            flash(msg_p, "error"); return render_template("register.html", levels=LEVELS)

        if User.query.filter_by(username=username.strip()).first():
            flash("Username already exists.", "error"); return render_template("register.html", levels=LEVELS)

        user = create_user(username, password)
        login_user(user)
        return redirect(url_for("web.dashboard"))
    return render_template("register.html", levels=LEVELS)

@web_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = verify_user(username, password)
        if not user:
            flash("Invalid username or password.", "error")
            return render_template("login.html")
        login_user(user)
        # auto-import some beginner words on first login
        if Word.query.filter_by(user_id=user.id).count() == 0:
            import_random_words(user, k=60, include_lower=True)
        return redirect(url_for("web.dashboard"))
    return render_template("login.html")

@web_bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web.login"))

@web_bp.get("/dashboard")
@login_required
def dashboard():
    total_words = Word.query.filter_by(user_id=current_user.id).count()
    total_attempts = Attempt.query.filter_by(user_id=current_user.id).count()
    return render_template("dashboard.html", total_words=total_words, total_attempts=total_attempts, level=current_user.level)

@web_bp.route("/settings", methods=["GET","POST"])
@login_required
def settings():
    if request.method == "POST":
        level = clamp_level(request.form.get("level","Beginner"))
        k = int(request.form.get("k", "50") or "50")
        include_lower = True if request.form.get("include_lower") == "on" else False

        set_user_level(current_user, level)
        added = import_random_words(current_user, k=k, include_lower=include_lower)
        flash(f"Saved! Level={level}. Imported {added} new words.", "success")
        return redirect(url_for("web.settings"))

    return render_template("settings.html", levels=LEVELS, current_level=current_user.level)

@web_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        prompt = (request.form.get("prompt") or "").strip()
        answer = (request.form.get("answer") or "").strip()
        level = clamp_level(request.form.get("level") or "Beginner")

        if not prompt or not answer:
            flash("Both fields are required.", "error")
            return render_template("add_word.html", levels=LEVELS)

        add_word(current_user.id, prompt, answer, level=level)
        flash("Word added!", "success")
        return redirect(url_for("web.add"))
    return render_template("add_word.html", levels=LEVELS)

@web_bp.get("/training")
@login_required
def training():
    max_rank = LEVEL_RANK.get(current_user.level, 0)
    word = pick_next_word(current_user.id, max_level_rank=max_rank)
    if not word:
        flash("No words yet. Go to Settings and import words.", "error")
        return redirect(url_for("web.settings"))
    return render_template("training.html", word=word)

@web_bp.post("/training/submit")
@login_required
def training_submit():
    word_id = request.form.get("word_id", type=int)
    user_input = (request.form.get("user_input") or "").strip()

    word = Word.query.filter_by(id=word_id, user_id=current_user.id).first()
    if not word:
        flash("Word not found.", "error")
        return redirect(url_for("web.training"))

    is_correct = check_answer(word, user_input)
    record_attempt(current_user, word, user_input, is_correct)

    current_app.logger.info("Attempt user=%s word_id=%s correct=%s", current_user.id, word.id, is_correct)

    if is_correct:
        flash("Correct ✅", "success")
    else:
        flash(f"Wrong ❌ Correct answer: {word.answer}", "error")

    return redirect(url_for("web.training"))

@web_bp.get("/stats")
@login_required
def stats():
    charts = generate_charts_for_user(current_user.id)
    return render_template("stats.html", charts=charts)
