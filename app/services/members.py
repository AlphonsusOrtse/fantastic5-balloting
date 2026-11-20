
import secrets

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Member


def create_member(name):
    """Create a member and return their one-time access code."""

    access_code = secrets.token_urlsafe(12)

    member = Member(
        name=name,
        access_code_hash=generate_password_hash(access_code)
    )

    db.session.add(member)
    db.session.commit()

    return member, access_code
