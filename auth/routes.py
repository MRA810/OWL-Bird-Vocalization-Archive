from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User
from utils import allowed_image, save_file, generate_tag

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("public.home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # Validations
        if not all([name, username, email, password]):
            flash("All fields are required.", "error")
            return render_template("auth/signup.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("auth/signup.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("auth/signup.html")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return render_template("auth/signup.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template("auth/signup.html")

        # Generate unique tag
        tag = generate_tag(username)
        while User.query.filter_by(tag=tag).first():
            tag = generate_tag(username)

        # Handle profile picture
        profile_image = "default.png"
        if "profile_image" in request.files:
            file = request.files["profile_image"]
            if file and file.filename and allowed_image(file.filename):
                profile_image = save_file(file, "profile_pics")

        user = User(
            name=name,
            username=username,
            tag=tag,
            email=email,
            password_hash=generate_password_hash(password),
            profile_image=profile_image,
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome to OWL, {user.name}!", "success")
        return redirect(url_for("public.home"))

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("public.home"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get("remember"))
            next_page = request.args.get("next")
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(next_page or url_for("public.home"))
        else:
            flash("Invalid credentials. Please try again.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "info")
    return redirect(url_for("public.home"))
