from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from models.user_model import get_user_by_email, create_visitor, authenticate_user

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


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login for Security Officers and Visitors."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Check for empty credentials
        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html", email=email)

        # Authenticate user credentials
        user = authenticate_user(email, password)
        if not user:
            flash("Invalid email or password.", "error")
            return render_template("login.html", email=email)

        # Establish user session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["role"] = user["role"]

        # Role-based dashboard redirect
        if user["role"] == "Security Officer":
            return redirect(url_for("dashboard.officer_dashboard"))
        elif user["role"] == "Visitor":
            return redirect(url_for("dashboard.visitor_dashboard"))
        else:
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout", methods=["GET"])
def logout():
    """Clear the session completely and redirect to login."""
    session.clear()
    session.modified = True
    return redirect(url_for("auth.login"))

