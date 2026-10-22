"""
database.py - MySQL connection + automatic table creation.
Rebuilt from the compiled database.cpython-314.pyc of the original project.
Set your own MySQL password in the MYSQL_PASSWORD environment variable,
or edit the DEFAULT_PASSWORD line below.
"""
import os
import mysql.connector

DATABASE_NAME = "ai_student_dashboard"

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
DEFAULT_PASSWORD = ""
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", DEFAULT_PASSWORD)


def get_connection():
    """Open a connection to the project database."""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DATABASE_NAME,
    )


def add_column(cursor, table, column, definition):
    """Add a column only if it does not exist (safe upgrade of old tables)."""
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
        """,
        (DATABASE_NAME, table, column),
    )
    exists = cursor.fetchone()[0]
    if not exists:
        cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}")


def initialize_database():
    """Create the database and all tables if they are not there yet."""
    server_connection = mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD
    )
    cursor = server_connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    cursor.close()
    server_connection.close()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(128) NOT NULL,
            name VARCHAR(100) NOT NULL,
            class_name VARCHAR(10),
            section VARCHAR(5),
            academic_year VARCHAR(20),
            gender VARCHAR(30),
            stream VARCHAR(50),
            subjects TEXT,
            date_of_birth DATE,
            email VARCHAR(150),
            phone VARCHAR(30)
        )
    """)
    add_column(cursor, "students", "class_name", "VARCHAR(10)")
    add_column(cursor, "students", "date_of_birth", "DATE")
    add_column(cursor, "students", "email", "VARCHAR(150)")
    add_column(cursor, "students", "phone", "VARCHAR(30)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject VARCHAR(255) NOT NULL,
            topic VARCHAR(255) NOT NULL,
            duration INT NOT NULL,
            priority VARCHAR(20) NOT NULL,
            deadline DATE NOT NULL,
            study_date DATE NOT NULL,
            added_on DATETIME NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            completed_at DATETIME,
            xp_awarded BOOLEAN DEFAULT FALSE
        )
    """)
    add_column(cursor, "study_tasks", "student_id", "INT")
    add_column(cursor, "study_tasks", "completed_at", "DATETIME")
    add_column(cursor, "study_tasks", "xp_awarded", "BOOLEAN DEFAULT FALSE")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_preferences (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT UNIQUE,
            wake_time TIME NOT NULL,
            sleep_time TIME NOT NULL,
            break_duration INT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deleted_tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            task_id INT,
            subject VARCHAR(255),
            topic VARCHAR(255),
            duration INT,
            priority VARCHAR(20),
            deadline DATE,
            study_date DATE,
            added_on DATETIME,
            row_date DATE,
            start_time TIME,
            end_time TIME,
            row_duration INT,
            row_deadline DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            title VARCHAR(255) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            due_date DATE NOT NULL,
            description TEXT,
            priority VARCHAR(20),
            estimated_minutes INT,
            status VARCHAR(30) DEFAULT 'In Progress',
            completed_at DATETIME,
            xp_awarded BOOLEAN DEFAULT FALSE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xp_transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            activity_type VARCHAR(50) NOT NULL,
            activity_id INT,
            xp_earned INT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


# Runs once when the project starts: makes sure every table exists
initialize_database()
