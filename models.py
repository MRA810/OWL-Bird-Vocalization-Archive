from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    tag = db.Column(db.String(20), unique=True, nullable=False)  # e.g. JOSH#N77B
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_image = db.Column(db.String(256), default="default.png")
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    birds = db.relationship("Bird", backref="owner", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Bird(db.Model):
    __tablename__ = "birds"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bird_name = db.Column(db.String(120), nullable=False)
    image_path = db.Column(db.String(256), nullable=True)
    downloadable = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    audio_samples = db.relationship(
        "AudioSample", backref="bird", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Bird {self.bird_name}>"


class AudioSample(db.Model):
    __tablename__ = "audio_samples"

    id = db.Column(db.Integer, primary_key=True)
    bird_id = db.Column(db.Integer, db.ForeignKey("birds.id"), nullable=False)
    vocalization_type = db.Column(db.String(80), nullable=False)  # alarm, mating, song, etc.
    description = db.Column(db.Text, nullable=True)
    audio_path = db.Column(db.String(256), nullable=False)
    extra_info = db.Column(db.Text, nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AudioSample {self.vocalization_type} for Bird {self.bird_id}>"
