"""
auth.py - account creation and login (SHA-256 password hashing).
Rebuilt from the compiled auth.cpython-314.pyc of the original project.
"""
import hashlib
from database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_account(username, password, name):
    """Insert a new student. Returns (success, message)."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO students (username, password_hash, name)
            VALUES (%s, %s, %s)
            """,
            (username, hash_password(password), name),
        )
        connection.commit()
        return True, "Account created successfully!"
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, "Username already exists."
        return False, "Something went wrong."
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def login_user(username, password):
    """Return {id, username, name} if the credentials match, else None."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, username, name
        FROM students
        WHERE username = %s AND password_hash = %s
        """,
        (username, hash_password(password)),
    )
    student = cursor.fetchone()
    cursor.close()
    connection.close()
    return student
