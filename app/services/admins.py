
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app.extensions import db
from app.models import Admin


def create_admin(username, password):
    """Create an administrator with a hashed password."""

    existing_admin = Admin.query.filter_by(
        username=username
    ).first()

    if existing_admin:
        raise ValueError("This admin username already exists.")

    admin = Admin(
        username=username,
        password_hash=generate_password_hash(password)
    )

    db.session.add(admin)
    db.session.commit()

    return admin


def authenticate_admin(username, password):
    """Authenticate an administrator."""

    admin = Admin.query.filter_by(
        username=username
    ).first()

    if admin and check_password_hash(
        admin.password_hash,
        password
    ):
        return admin

    return None
