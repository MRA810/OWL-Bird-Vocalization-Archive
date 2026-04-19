import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

print("DATABASE_URL from env:", os.environ.get("DATABASE_URL", "NOT SET"), flush=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "a8G8GvNKQMvTFCte4PFwQKTEKmrWUKKT")

    _db_url = os.environ.get("DATABASE_URL", "postgresql://owl_db_h9te_user:a8G8GvNKQMvTFCte4PFwQKTEKmrWUKKT@dpg-d7iho8vavr4c73fnehng-a/owl_db_h9te")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    PROFILE_PICS_FOLDER = os.path.join(UPLOAD_FOLDER, "profile_pics")
    BIRD_IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, "bird_images")
    AUDIOS_FOLDER = os.path.join(UPLOAD_FOLDER, "audios")

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload

    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "ogg", "flac", "m4a", "aac"}