
from datetime import datetime

from app.extensions import db


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    # Store only the hashed access code, never the original code.
    access_code_hash = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    assignments = db.relationship(
        "BallotAssignment",
        back_populates="member",
        cascade="all, delete-orphan"
    )


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


class BallotSession(db.Model):
    __tablename__ = "ballot_sessions"

    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="closed"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    opened_at = db.Column(db.DateTime, nullable=True)
    closed_at = db.Column(db.DateTime, nullable=True)

    assignments = db.relationship(
        "BallotAssignment",
        back_populates="session",
        cascade="all, delete-orphan"
    )


class BallotAssignment(db.Model):
    __tablename__ = "ballot_assignments"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("ballot_sessions.id"),
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    number = db.Column(db.Integer, nullable=False)

    drawn_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    session = db.relationship(
        "BallotSession",
        back_populates="assignments"
    )

    member = db.relationship(
        "Member",
        back_populates="assignments"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "session_id",
            "member_id",
            name="unique_member_per_session"
        ),
        db.UniqueConstraint(
            "session_id",
            "number",
            name="unique_number_per_session"
        ),
        db.CheckConstraint(
            "number >= 1 AND number <= 5",
            name="valid_ballot_number"
        ),
    )
