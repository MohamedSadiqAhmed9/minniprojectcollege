from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/officer/dashboard", methods=["GET"])
def officer_dashboard():
    """Security Officer landing page after login."""
    if "user_id" not in session or session.get("role") != "Security Officer":
        return redirect(url_for("auth.login"))

    return render_template(
        "officer_dashboard.html",
        user_name=session.get("user_name"),
        role=session.get("role"),
    )


@dashboard_bp.route("/visitor/dashboard", methods=["GET"])
def visitor_dashboard():
    """Visitor landing page after login."""
    if "user_id" not in session or session.get("role") != "Visitor":
        return redirect(url_for("auth.login"))

    return render_template(
        "visitor_dashboard.html",
        user_name=session.get("user_name"),
        role=session.get("role"),
    )
