from flask import Blueprint, redirect, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    """Root route redirects to login."""
    return redirect(url_for("auth.login"), code=302)

