import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Locate .env in the same directory as this script
env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path, override=True)

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE = os.getenv("MYSQL_DATABASE", "Student_portal")

if not MYSQL_PASSWORD:
    raise RuntimeError(
        f"MYSQL_PASSWORD is missing. Check your .env file: {env_path}"
    )

# Sample data: name, class, English, Maths, Science
students = [
    ("Arun", "10-A", 85, 90, 78),
    ("Priya", "10-A", 95, 92, 96),
    ("Kumar", "10-B", 65, 70, 72),
    ("Divya", "10-B", 45, 55, 60),
    ("Ravi", "10-A", 30, 80, 75),
]


def calculate_grade(english, maths, science):
    """Return a grade using the example rules below."""
    marks = [english, maths, science]

    # Example rule: a score below 35 in any subject is a fail.
    if any(mark < 35 for mark in marks):
        return "F"

    average = sum(marks) / len(marks)

    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def validate_marks(name, marks):
    """Ensure every mark is an integer from 0 through 100."""
    for mark in marks:
        if not isinstance(mark, int) or not 0 <= mark <= 100:
            raise ValueError(f"Invalid mark for {name}: {mark}. Marks must be integers from 0 to 100.")


connection = None
cursor = None

try:
    # 1. Authenticate to MySQL server.
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )

    if not connection.is_connected():
        raise RuntimeError("Could not connect to MySQL.")

    print("MySQL authentication successful!")

    cursor = connection.cursor()

    cursor.execute(f"USE `{DATABASE}`")

    # 3. Create the Students table if it does not exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            class_name VARCHAR(20) NOT NULL,
            english INT NOT NULL,
            maths INT NOT NULL,
            science INT NOT NULL,
            total INT NOT NULL,
            grade VARCHAR(2) NOT NULL,
            UNIQUE KEY unique_student (student_name, class_name),
            CHECK (english BETWEEN 0 AND 100),
            CHECK (maths BETWEEN 0 AND 100),
            CHECK (science BETWEEN 0 AND 100)
        )
    """)

    # 4. Insert new students or update their marks if the same
    #    student_name + class_name already exists.
    insert_query = """
        INSERT INTO Students
            (student_name, class_name, english, maths, science, total, grade)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            english = %s,
            maths = %s,
            science = %s,
            total = %s,
            grade = %s
    """
    for name, class_name, english, maths, science in students:
        marks = [english, maths, science]
        validate_marks(name, marks)

        total = sum(marks)
        grade = calculate_grade(english, maths, science)

        values = (
            name, class_name, english, maths, science, total, grade,
            english, maths, science, total, grade
        )
        cursor.execute(insert_query, values)

    connection.commit()
    print("Student records saved successfully!")

    # Retrieve and display student records
    cursor.execute("""
        SELECT student_id, student_name, class_name,
               english, maths, science, total, grade
        FROM Students
        ORDER BY student_id
    """)

    rows = cursor.fetchall()

    print("\nSTUDENT PORTAL")
    print("-" * 80)
    print(
        f"{'ID':<4} {'Name':<12} {'Class':<8} "
        f"{'English':>7} {'Maths':>7} {'Science':>8} "
        f"{'Total':>7} {'Grade':>6}"
    )
    print("-" * 80)

    for row in rows:
        print(
            f"{row[0]:<4} {row[1]:<12} {row[2]:<8} "
            f"{row[3]:>7} {row[4]:>7} {row[5]:>8} "
            f"{row[6]:>7} {row[7]:>6}"
        )

except (Error, ValueError, RuntimeError) as error:
    if connection and connection.is_connected():
        connection.rollback()
    print(f"Error: {error}")

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("\nMySQL connection closed.")