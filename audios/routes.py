from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import Bird, AudioSample
from utils import allowed_audio, save_file, delete_file

audios_bp = Blueprint("audios", __name__)

VOCALIZATION_TYPES = ["song", "call", "alarm", "mating", "contact", "flight", "feeding", "other"]


@audios_bp.route("/audio/<int:bird_id>/upload", methods=["GET", "POST"])
@login_required
def upload_audio(bird_id):
    bird = Bird.query.get_or_404(bird_id)
    if bird.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        vocalization_type = request.form.get("vocalization_type", "").strip()
        description = request.form.get("description", "").strip()
        extra_info = request.form.get("extra_info", "").strip()

        if not vocalization_type:
            flash("Vocalization type is required.", "error")
            return render_template(
                "audios/audio_form.html",
                action="Upload",
                bird=bird,
                audio=None,
                vocalization_types=VOCALIZATION_TYPES,
            )

        if "audio_file" not in request.files or not request.files["audio_file"].filename:
            flash("An audio file is required.", "error")
            return render_template(
                "audios/audio_form.html",
                action="Upload",
                bird=bird,
                audio=None,
                vocalization_types=VOCALIZATION_TYPES,
            )

        file = request.files["audio_file"]
        if not allowed_audio(file.filename):
            flash("Invalid audio format. Allowed: mp3, wav, ogg, flac, m4a, aac", "error")
            return render_template(
                "audios/audio_form.html",
                action="Upload",
                bird=bird,
                audio=None,
                vocalization_types=VOCALIZATION_TYPES,
            )

        audio_path = save_file(file, "audios")
        audio = AudioSample(
            bird_id=bird.id,
            vocalization_type=vocalization_type,
            description=description,
            audio_path=audio_path,
            extra_info=extra_info,
        )
        db.session.add(audio)
        db.session.commit()

        flash("Audio sample uploaded successfully!", "success")
        return redirect(url_for("public.bird_page", bird_id=bird.id))

    return render_template(
        "audios/audio_form.html",
        action="Upload",
        bird=bird,
        audio=None,
        vocalization_types=VOCALIZATION_TYPES,
    )


@audios_bp.route("/audio/<int:audio_id>/edit", methods=["GET", "POST"])
@login_required
def edit_audio(audio_id):
    audio = AudioSample.query.get_or_404(audio_id)
    bird = audio.bird
    if bird.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        audio.vocalization_type = request.form.get("vocalization_type", "").strip()
        audio.description = request.form.get("description", "").strip()
        audio.extra_info = request.form.get("extra_info", "").strip()

        if "audio_file" in request.files:
            file = request.files["audio_file"]
            if file and file.filename and allowed_audio(file.filename):
                delete_file(audio.audio_path, "audios")
                audio.audio_path = save_file(file, "audios")

        db.session.commit()
        flash("Audio sample updated.", "success")
        return redirect(url_for("public.bird_page", bird_id=bird.id))

    return render_template(
        "audios/audio_form.html",
        action="Edit",
        bird=bird,
        audio=audio,
        vocalization_types=VOCALIZATION_TYPES,
    )


@audios_bp.route("/audio/<int:audio_id>/delete", methods=["POST"])
@login_required
def delete_audio(audio_id):
    audio = AudioSample.query.get_or_404(audio_id)
    bird = audio.bird
    if bird.user_id != current_user.id:
        abort(403)

    delete_file(audio.audio_path, "audios")
    db.session.delete(audio)
    db.session.commit()
    flash("Audio sample deleted.", "success")
    return redirect(url_for("public.bird_page", bird_id=bird.id))


@audios_bp.route("/audio/<int:audio_id>/hide", methods=["POST"])
@login_required
def hide_audio(audio_id):
    audio = AudioSample.query.get_or_404(audio_id)
    bird = audio.bird
    if bird.user_id != current_user.id:
        abort(403)

    audio.is_hidden = not audio.is_hidden
    db.session.commit()
    status = "hidden" if audio.is_hidden else "visible"
    flash(f"Audio sample is now {status}.", "success")
    return redirect(url_for("public.bird_page", bird_id=bird.id))
