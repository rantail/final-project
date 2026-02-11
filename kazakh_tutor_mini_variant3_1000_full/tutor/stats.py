import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import current_app
from .models import Word, Attempt

def _save_fig(fig, filename: str) -> str:
    out_path = os.path.join(current_app.config["GENERATED_DIR"], filename)
    fig.savefig(out_path, bbox_inches="tight", dpi=140)
    plt.close(fig)
    return f"generated/{filename}"

def generate_charts_for_user(user_id: int):
    words = Word.query.filter_by(user_id=user_id).all()
    atts = Attempt.query.filter_by(user_id=user_id).order_by(Attempt.created_at.asc()).all()

    if not words:
        return {"message": "No data yet. Import words and train."}

    rows = [{"created_at": a.created_at, "is_correct": 1 if a.is_correct else 0, "word_id": a.word_id} for a in atts]
    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["created_at", "is_correct", "word_id"])
    charts = {}

    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["rolling_acc"] = df["is_correct"].rolling(window=10, min_periods=1).mean()
        fig = plt.figure()
        plt.plot(df["created_at"], df["rolling_acc"])
        plt.title("Rolling Accuracy (last 10 attempts)")
        plt.xlabel("Time")
        plt.ylabel("Accuracy")
        charts["rolling_accuracy"] = _save_fig(fig, "rolling_accuracy.png")

    mistake_counts = {w.prompt: max(0, w.times_shown - w.times_correct) for w in words}
    top = sorted(mistake_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    labels = [x[0] for x in top]
    values = [x[1] for x in top]

    fig = plt.figure()
    plt.bar(labels, values)
    plt.title("Top Mistakes")
    plt.xlabel("Word")
    plt.ylabel("Mistakes")
    plt.xticks(rotation=30, ha="right")
    charts["top_mistakes"] = _save_fig(fig, "top_mistakes.png")

    total_shown = sum(w.times_shown for w in words)
    total_correct = sum(w.times_correct for w in words)
    acc = (total_correct / total_shown) if total_shown else 0.0

    charts["summary"] = {
        "total_words": len(words),
        "total_attempts": len(atts),
        "overall_accuracy": round(acc * 100, 2)
    }
    return charts
