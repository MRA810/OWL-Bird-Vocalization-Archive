import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "owl-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://owl_user:owl_pass@localhost/owl_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    PROFILE_PICS_FOLDER = os.path.join(UPLOAD_FOLDER, "profile_pics")
    BIRD_IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, "bird_images")
    AUDIOS_FOLDER = os.path.join(UPLOAD_FOLDER, "audios")

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload

    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "ogg", "flac", "m4a", "aac"}
