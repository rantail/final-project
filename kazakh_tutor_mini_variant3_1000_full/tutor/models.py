from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(12), default="Beginner")  # Beginner/A1/A2/B1/B2

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    words = db.relationship("Word", backref="user", lazy=True, cascade="all, delete-orphan")
    attempts = db.relationship("Attempt", backref="user", lazy=True, cascade="all, delete-orphan")

class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    prompt = db.Column(db.String(160), nullable=False)
    answer = db.Column(db.String(160), nullable=False)
    level = db.Column(db.String(12), default="Beginner")  # imported level

    times_shown = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)

    last_seen_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship("Attempt", backref="word", lazy=True, cascade="all, delete-orphan")

class Attempt(db.Model):
    __tablename__ = "attempts"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False, index=True)

    user_input = db.Column(db.String(160), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    seconds_since_last = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
