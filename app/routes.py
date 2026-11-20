from app.services.admins import authenticate_admin
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from app.services.members import authenticate_member

main = Blueprint("main", __name__)


def member_required(view):
    """Protect a route so only authenticated members can access it."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "member_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("main.login"))

        return view(*args, **kwargs)

    return wrapped_view



def admin_required(view):
    """Protect routes so only administrators can access them."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "admin_id" not in session:
            flash("Administrator login required.", "error")
            return redirect(url_for("main.admin_login"))

        return view(*args, **kwargs)

    return wrapped_view



@main.route("/")
def home():
    if "member_id" in session:
        return render_template(
            "home.html",
            member_name=session.get("member_name")
        )

    return redirect(url_for("main.login"))


@main.route("/login", methods=["GET", "POST"])
def login():
    if "member_id" in session:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        access_code = request.form.get("access_code", "").strip()

        if not access_code:
            flash("Please enter your access code.", "error")
            return render_template("login.html")

        member = authenticate_member(access_code)

        if member is None:
            flash("Invalid access code. Please try again.", "error")
            return render_template("login.html")

        session.clear()
        session["member_id"] = member.id
        session["member_name"] = member.name

        flash(f"Welcome, {member.name}!", "success")
        return redirect(url_for("main.home"))

    return render_template("login.html")


@main.route("/logout", methods=["POST"])
@member_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.login"))


@main.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if "admin_id" in session:
        return redirect(url_for("main.admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = authenticate_admin(username, password)

        if admin is None:
            flash("Invalid administrator credentials.", "error")
            return render_template("admin_login.html")

        session.clear()
        session["admin_id"] = admin.id
        session["admin_username"] = admin.username

        flash("Administrator login successful.", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin_login.html")


@main.route("/admin")
@admin_required
def admin_dashboard():
    from app.models import Member

    members = Member.query.order_by(Member.id).all()

    return render_template(
        "admin_dashboard.html",
        members=members,
        admin_username=session.get("admin_username")
    )


@main.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():
    session.clear()
    flash("Administrator logged out.", "success")
    return redirect(url_for("main.admin_login"))

