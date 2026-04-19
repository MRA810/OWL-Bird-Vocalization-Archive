from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import Bird
from utils import allowed_image, save_file, delete_file

birds_bp = Blueprint("birds", __name__)


@birds_bp.route("/bird/create", methods=["GET", "POST"])
@login_required
def create_bird():
    if request.method == "POST":
        bird_name = request.form.get("bird_name", "").strip()
        description = request.form.get("description", "").strip()
        downloadable = request.form.get("downloadable") == "on"

        if not bird_name:
            flash("Bird name is required.", "error")
            return render_template("birds/bird_form.html", action="Create", bird=None)

        image_path = None
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_image(file.filename):
                image_path = save_file(file, "bird_images")

        bird = Bird(
            user_id=current_user.id,
            bird_name=bird_name,
            description=description,
            downloadable=downloadable,
            image_path=image_path,
        )
        db.session.add(bird)
        db.session.commit()

        flash(f'"{bird_name}" has been added to the archive!', "success")
        return redirect(url_for("public.bird_page", bird_id=bird.id))

    return render_template("birds/bird_form.html", action="Create", bird=None)


@birds_bp.route("/bird/<int:bird_id>/edit", methods=["GET", "POST"])
@login_required
def edit_bird(bird_id):
    bird = Bird.query.get_or_404(bird_id)
    if bird.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        bird.bird_name = request.form.get("bird_name", "").strip()
        bird.description = request.form.get("description", "").strip()
        bird.downloadable = request.form.get("downloadable") == "on"

        if not bird.bird_name:
            flash("Bird name is required.", "error")
            return render_template("birds/bird_form.html", action="Edit", bird=bird)

        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_image(file.filename):
                delete_file(bird.image_path, "bird_images")
                bird.image_path = save_file(file, "bird_images")

        db.session.commit()
        flash("Bird updated successfully.", "success")
        return redirect(url_for("public.bird_page", bird_id=bird.id))

    return render_template("birds/bird_form.html", action="Edit", bird=bird)


@birds_bp.route("/bird/<int:bird_id>/delete", methods=["POST"])
@login_required
def delete_bird(bird_id):
    bird = Bird.query.get_or_404(bird_id)
    if bird.user_id != current_user.id:
        abort(403)

    # Delete associated files
    if bird.image_path:
        delete_file(bird.image_path, "bird_images")
    for audio in bird.audio_samples:
        delete_file(audio.audio_path, "audios")

    db.session.delete(bird)
    db.session.commit()
    flash(f'"{bird.bird_name}" has been permanently deleted.', "success")
    return redirect(url_for("public.profile", username=current_user.username))


@birds_bp.route("/bird/<int:bird_id>/hide", methods=["POST"])
@login_required
def hide_bird(bird_id):
    bird = Bird.query.get_or_404(bird_id)
    if bird.user_id != current_user.id:
        abort(403)

    bird.is_hidden = not bird.is_hidden
    db.session.commit()
    status = "hidden" if bird.is_hidden else "visible"
    flash(f'"{bird.bird_name}" is now {status}.', "success")
    return redirect(url_for("public.bird_page", bird_id=bird.id))
