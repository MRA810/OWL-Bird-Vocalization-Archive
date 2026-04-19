import os
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directories exist
    os.makedirs(app.config["PROFILE_PICS_FOLDER"], exist_ok=True)
    os.makedirs(app.config["BIRD_IMAGES_FOLDER"], exist_ok=True)
    os.makedirs(app.config["AUDIOS_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from auth.routes import auth_bp
    from birds.routes import birds_bp
    from audios.routes import audios_bp
    from public.routes import public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(birds_bp)
    app.register_blueprint(audios_bp)
    app.register_blueprint(public_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
