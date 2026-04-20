# import os
# from dotenv import load_dotenv

# load_dotenv()

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# print("DATABASE_URL from env:", os.environ.get("DATABASE_URL", "NOT SET"), flush=True)


# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "npg_igfw5ndh3apE")

#     _db_url = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_igfw5ndh3apE@ep-lingering-firefly-aou2jr9m-pooler.c-2.ap-southeast-1.aws.neon.tech/owl_db?sslmode=require&channel_binding=require")
#     if _db_url.startswith("postgres://"):
#         _db_url = _db_url.replace("postgres://", "postgresql://", 1)
#     SQLALCHEMY_DATABASE_URI = _db_url

#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
#     PROFILE_PICS_FOLDER = os.path.join(UPLOAD_FOLDER, "profile_pics")
#     BIRD_IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, "bird_images")
#     AUDIOS_FOLDER = os.path.join(UPLOAD_FOLDER, "audios")

#     MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload

#     ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
#     ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "ogg", "flac", "m4a", "aac"}
    
    
#     import os
# from dotenv import load_dotenv

# load_dotenv()

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "npg_igfw5ndh3apE")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is not set.")

    _db_url = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_igfw5ndh3apE@ep-lingering-firefly-aou2jr9m-pooler.c-2.ap-southeast-1.aws.neon.tech/owl_db?sslmode=require&channel_binding=require")
    if not _db_url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
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