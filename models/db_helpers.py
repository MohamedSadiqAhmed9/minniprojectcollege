from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from models import db


def execute_query(query, params=None):
    try:
        result = db.session.execute(text(query), params or {})
        db.session.commit()
        return result
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error
    except Exception as error:
        db.session.rollback()
        raise error


def insert_record(query, params=None):
    try:
        result = db.session.execute(text(query), params or {})
        db.session.commit()
        return result.lastrowid
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error
    except Exception as error:
        db.session.rollback()
        raise error


def update_record(query, params=None):
    try:
        result = db.session.execute(text(query), params or {})
        db.session.commit()
        return result.rowcount
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error
    except Exception as error:
        db.session.rollback()
        raise error


def delete_record(query, params=None):
    try:
        result = db.session.execute(text(query), params or {})
        db.session.commit()
        return result.rowcount
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error
    except Exception as error:
        db.session.rollback()
        raise error


def fetch_records(query, params=None):
    try:
        result = db.session.execute(text(query), params or {})
        return result.fetchall()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error
    except Exception as error:
        db.session.rollback()
        raise error
