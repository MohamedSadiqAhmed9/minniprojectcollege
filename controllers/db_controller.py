from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from models import db

db_bp = Blueprint("db", __name__)


@db_bp.route("/test-db", methods=["GET"])
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "success", "message": "Database Connected"}), 200
    except SQLAlchemyError as error:
        db.session.rollback()
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Database Connection Failed",
                    "detail": str(error),
                }
            ),
            500,
        )
    except Exception as error:
        db.session.rollback()
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Database Connection Failed",
                    "detail": str(error),
                }
            ),
            500,
        )
