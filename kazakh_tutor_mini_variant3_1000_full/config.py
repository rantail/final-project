import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "kazakh_tutor.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
    GENERATED_DIR = os.path.join(BASE_DIR, "tutor", "static", "generated")
    GLOBAL_WORDS_PATH = os.path.join(BASE_DIR, "tutor", "data", "global_1000_words.json")
