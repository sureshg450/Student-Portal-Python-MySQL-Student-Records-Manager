# Student-Portal-Python-MySQL-Student-Records-Manager

# Student Portal

A command-line student portal built with Python and MySQL. It validates student marks, calculates totals and grades, stores records in a MySQL database, and displays the saved records in a formatted table.

## Features

- Creates the `Students` table when it does not already exist.
- Validates that marks are integers from 0 to 100.
- Calculates totals and grades for English, Maths, and Science.
- Inserts sample student records and updates their marks on later runs.
- Displays saved student records in the terminal.

## Requirements

- Python 3
- A running MySQL server and a MySQL user with access to the project database

## Setup

1. Clone or download this repository and open a terminal in the project directory.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the Python dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create the database in MySQL if it does not already exist:

   ```sql
   CREATE DATABASE Student_portal;
   ```

5. Create a `.env` file in the project directory with your MySQL connection settings:

   ```env
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=Student_portal
   ```

   Update the values to match your local MySQL setup. Keep `.env` private and do not upload credentials to GitHub.

## Run

```powershell
python student_portal.py
```

The script inserts or updates its sample records, then prints the records currently stored in the `Students` table.

## Grade scale

A mark below 35 in any subject results in an `F`. Otherwise, the grade is based on the average mark:

| Average | Grade |
| --- | --- |
| 90–100 | A+ |
| 80–89 | A |
| 70–79 | B |
| 60–69 | C |
| 50–59 | D |
| Below 50 | F |

<img width="929" height="232" alt="image" src="https://github.com/user-attachments/assets/716e0dab-0c6f-4dca-9994-ebb922c3f521" />

## Project files

- `student_portal.py` — database setup, mark validation, grade calculation, and terminal output.
- `requirements.txt` — Python package dependencies.
