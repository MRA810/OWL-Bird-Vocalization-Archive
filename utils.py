import os
import uuid
import random
import string
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
    )


def allowed_audio(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_AUDIO_EXTENSIONS"]
    )


def save_file(file, subfolder):
    """Save a file to the uploads directory and return its filename."""
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, unique_name))
    return unique_name


def delete_file(filename, subfolder):
    """Delete a file from the uploads directory."""
    if filename and filename != "default.png":
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder, filename)
        if os.path.exists(path):
            os.remove(path)


def generate_tag(username):
    """Generate a unique tag like JOSH#N77B."""
    prefix = username[:4].upper()
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}#{suffix}"
