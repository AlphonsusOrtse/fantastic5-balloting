
import os

from flask import Flask
from dotenv import load_dotenv

from app.extensions import db


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "development-only-change-this"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///fantastic5.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from app import models
        db.create_all()

    return app
