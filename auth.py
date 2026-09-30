import hashlib
import os
from database import get_connection


def hash_password(password: str, salt: str = None) -> tuple:
    """Hashes a password with a salt. Generates a new salt if none is given."""
    if salt is None:
        salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000  # number of iterations — higher is slower but more secure
    )
    return hashed.hex(), salt


def create_user(username: str, password: str, role: str):
    """Creates a new user with a hashed password."""
    password_hash, salt = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
            (username, password_hash, salt, role)
        )
        conn.commit()
        print(f"User '{username}' created with role '{role}'.")
    except Exception as e:
        print(f"Error creating user '{username}': {e}")
    finally:
        conn.close()


def verify_login(username: str, password: str):
    """Checks a username/password pair against the database.
    Returns the user's role if valid, otherwise None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    hashed_attempt, _ = hash_password(password, salt=user["salt"])
    if hashed_attempt == user["password_hash"]:
        return user["role"]
    return None

if __name__ == "__main__":
    pass  # test code removed — user creation now handled in seed_data.py    