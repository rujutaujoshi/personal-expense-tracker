
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "expenses.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL CHECK (amount > 0),
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        """)


def add_expense(amount, category, description, expense_date):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO expenses
                (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        """, (amount, category, description, expense_date))


def get_expenses(month):
    with get_connection() as connection:
        return connection.execute("""
            SELECT *
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            ORDER BY date DESC, id DESC
        """, (month,)).fetchall()


def delete_expense(expense_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )


def get_total_expenses(month):
    with get_connection() as connection:
        result = connection.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE substr(date, 1, 7) = ?
        """, (month,)).fetchone()

        return result[0]


def get_category_summary(month):
    with get_connection() as connection:
        return connection.execute("""
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            GROUP BY category
            ORDER BY total DESC
        """, (month,)).fetchall()


def get_monthly_summary(year):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT substr(date, 6, 2) AS month,
                   SUM(amount) AS total
            FROM expenses
            WHERE substr(date, 1, 4) = ?
            GROUP BY substr(date, 6, 2)
            ORDER BY month
        """, (str(year),)).fetchall()

    totals = [0.0] * 12

    for row in rows:
        month_index = int(row["month"]) - 1
        totals[month_index] = row["total"]

    return totals
