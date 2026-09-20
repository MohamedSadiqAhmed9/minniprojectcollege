from flask import Blueprint, render_template, request, flash
from models.user_model import get_user_by_email, create_visitor

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        mobile_number = request.form.get("mobile_number", "").strip()

        # Validation 1: Check for empty fields
        if not name or not email or not password or not mobile_number:
            flash("All fields are required.", "error")
            return render_template(
                "register.html",
                name=name,
                email=email,
                mobile_number=mobile_number,
            )

        # Validation 2: Email format (@ check)
        if "@" not in email:
            flash("Please enter a valid email address.", "error")
            return render_template(
                "register.html",
                name=name,
                email=email,
                mobile_number=mobile_number,
            )

        # Validation 3: Duplicate email check
        existing_user = get_user_by_email(email)
        if existing_user:
            flash("Email already registered.", "error")
            return render_template(
                "register.html",
                name=name,
                email=email,
                mobile_number=mobile_number,
            )

        # Successful registration
        create_visitor(name, email, password, mobile_number)
        flash("Registration successful. Please <strong>login</strong> to continue.", "success")
        return render_template("register.html")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET"])
def login():
    """Placeholder login route for upcoming tasks."""
    return render_template("login.html")
