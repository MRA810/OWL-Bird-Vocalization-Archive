import io
import os
import qrcode
import base64
from flask import (
    Blueprint, render_template, redirect, url_for,
    send_from_directory, abort, current_app, make_response
)
from flask_login import current_user
from models import Bird, AudioSample, User

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    birds = (
        Bird.query.filter_by(is_hidden=False)
        .order_by(Bird.created_at.desc())
        .limit(40)
        .all()
    )
    return render_template("public/home.html", birds=birds)


@public_bp.route("/bird/<int:bird_id>")
def bird_page(bird_id):
    bird = Bird.query.get_or_404(bird_id)

    # Allow owner to see hidden birds
    if bird.is_hidden and (not current_user.is_authenticated or current_user.id != bird.user_id):
        abort(404)

    # Filter audio samples — owner sees all, public sees visible only
    if current_user.is_authenticated and current_user.id == bird.user_id:
        audios = AudioSample.query.filter_by(bird_id=bird.id).order_by(AudioSample.created_at.desc()).all()
    else:
        audios = AudioSample.query.filter_by(bird_id=bird.id, is_hidden=False).order_by(AudioSample.created_at.desc()).all()

    is_owner = current_user.is_authenticated and current_user.id == bird.user_id
    return render_template("public/bird.html", bird=bird, audios=audios, is_owner=is_owner)


@public_bp.route("/u/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    is_owner = current_user.is_authenticated and current_user.id == user.id

    if is_owner:
        birds = Bird.query.filter_by(user_id=user.id).order_by(Bird.created_at.desc()).all()
    else:
        birds = Bird.query.filter_by(user_id=user.id, is_hidden=False).order_by(Bird.created_at.desc()).all()

    # Generate QR code for this profile URL
    profile_url = url_for("public.profile", username=username, _external=True)
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(profile_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#25343F", back_color="#EAEFFE")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    return render_template(
        "public/profile.html",
        user=user,
        birds=birds,
        is_owner=is_owner,
        qr_b64=qr_b64,
    )


@public_bp.route("/image/<path:filename>")
def serve_image(filename):
    """Direct image access — serves bird images as downloadable."""
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "bird_images")
    response = make_response(send_from_directory(folder, filename))
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@public_bp.route("/static/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
