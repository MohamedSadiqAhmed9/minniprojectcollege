import os
import urllib.parse
from flask import Flask
from dotenv import load_dotenv
from models import db
from controllers.main_controller import main_bp
from controllers.db_controller import db_bp
from controllers.auth_controller import auth_bp

load_dotenv()


def create_app():
    """Application factory for the Visitor Pass Management System."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load configuration
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "visitor_pass_db")

    # URL-encode user and password to handle special characters safely
    encoded_user = urllib.parse.quote_plus(db_user)
    encoded_password = urllib.parse.quote_plus(db_password)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{encoded_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "visitor-pass-secret-key-2026")

    # Initialize SQLAlchemy database object
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(auth_bp)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
