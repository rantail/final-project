import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager

from .models import db, User
from .routes_web import web_bp
from .routes_api import api_bp
from config import Config

login_manager = LoginManager()
login_manager.login_view = "web.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def _setup_folders(app: Flask):
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
        db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.makedirs(os.path.dirname(app.config["LOG_FILE"]), exist_ok=True)
    os.makedirs(app.config["GENERATED_DIR"], exist_ok=True)

def _setup_logging(app: Flask):
    handler = RotatingFileHandler(app.config["LOG_FILE"], maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.setLevel(logging.INFO)
    if not any(isinstance(h, RotatingFileHandler) for h in app.logger.handlers):
        app.logger.addHandler(handler)

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    _setup_folders(app)
    _setup_logging(app)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
