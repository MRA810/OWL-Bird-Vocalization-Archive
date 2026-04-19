import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "83e730bb4116a068b73e413c5e23df2328ba339581646b4f059dc9d0d5c6a6d5")
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
