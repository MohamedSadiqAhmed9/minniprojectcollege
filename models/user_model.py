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


def authenticate_user(email, password):
    """
    Look up a user by email, verify password, and return a dictionary
    with id, name, email, and role on success, or None on failure.
    """
    user = get_user_by_email(email)
    if not user:
        return None

    if hasattr(user, "_mapping"):
        mapping = user._mapping
        stored_password = mapping.get("password")
        if stored_password != password:
            return None
        return {
            "id": mapping.get("id"),
            "name": mapping.get("name"),
            "email": mapping.get("email"),
            "role": mapping.get("role"),
        }
    elif isinstance(user, dict):
        if user.get("password") != password:
            return None
        return {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "role": user.get("role"),
        }
    else:
        # Row / Tuple fallback
        stored_password = getattr(user, "password", None)
        if stored_password is None and hasattr(user, "__getitem__"):
            stored_password = user[3]
        if stored_password != password:
            return None

        user_id = getattr(user, "id", user[0] if hasattr(user, "__getitem__") else None)
        name = getattr(user, "name", user[1] if hasattr(user, "__getitem__") else None)
        email_val = getattr(user, "email", user[2] if hasattr(user, "__getitem__") else None)
        role = getattr(user, "role", user[5] if hasattr(user, "__getitem__") else None)

        return {
            "id": user_id,
            "name": name,
            "email": email_val,
            "role": role,
        }

