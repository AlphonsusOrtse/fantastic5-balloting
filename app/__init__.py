import click
import os

from flask import Flask
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

from app.extensions import db

csrf = CSRFProtect()


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
    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from app import models
        db.create_all()

    @app.cli.command("create-member")
    @click.argument("name")
    def create_member_command(name):
        """Create a participant and display their private access code."""

        from app.models import Member
        from app.services.members import create_member

        if Member.query.count() >= 5:
            click.echo("The ballot group already has five members.")
            return

        member, access_code = create_member(name)

        click.echo(f"Member created: {member.name}")
        click.echo(f"Private access code: {access_code}")
        click.echo("Share this code privately. It cannot be retrieved later.")

    return app
