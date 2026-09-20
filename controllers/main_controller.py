from flask import Blueprint, redirect, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    """Root route redirects to visitor registration."""
    return redirect(url_for("auth.register"), code=302)
