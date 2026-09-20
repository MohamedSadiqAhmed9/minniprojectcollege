from models import fetch_records, insert_record


def get_user_by_email(email):
    """Look up a user in the database by email address."""
    query = "SELECT * FROM users WHERE email = :email"
    records = fetch_records(query, {"email": email})
    return records[0] if records else None


def create_visitor(name, email, password, mobile_number):
    """Create a new visitor record in the users table."""
    query = """
        INSERT INTO users (name, email, password, mobile_number, role)
        VALUES (:name, :email, :password, :mobile_number, :role)
    """
    params = {
        "name": name,
        "email": email,
        "password": password,
        "mobile_number": mobile_number,
        "role": "Visitor",
    }
    return insert_record(query, params)
