
import os
from datetime import date, datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    init_db,
    add_expense,
    get_expenses,
    delete_expense,
    get_total_expenses,
    get_category_summary,
    get_monthly_summary
)

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "local-development-secret-change-before-deployment"
)

APP_VERSION = "1.0"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Education",
    "Health",
    "Other"
]

init_db()


def valid_month(value):
    try:
        datetime.strptime(value, "%Y-%m")
        return len(value) == 7
    except (ValueError, TypeError):
        return False


@app.route("/")
def dashboard():
    current_month = date.today().strftime("%Y-%m")

    selected_month = request.args.get(
        "month", current_month
    )

    if not valid_month(selected_month):
        selected_month = current_month

    selected_year = selected_month[:4]

    expenses = get_expenses(selected_month)
    total = get_total_expenses(selected_month)
    categories = get_category_summary(selected_month)
    monthly_totals = get_monthly_summary(selected_year)

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total=total,
        categories=categories,
        monthly_totals=monthly_totals,
        selected_month=selected_month,
        selected_year=selected_year,
        version=APP_VERSION,
        category_options=CATEGORIES,
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add():
    amount_text = request.form.get("amount", "")
    category = request.form.get("category", "")
    description = request.form.get(
        "description", ""
    ).strip()
    expense_date = request.form.get("date", "")

    selected_month = date.today().strftime("%Y-%m")

    try:
        amount = float(amount_text)

        if not 0 < amount < float("inf"):
            raise ValueError("Invalid amount")

        if category not in CATEGORIES:
            raise ValueError("Invalid category")

        parsed_date = date.fromisoformat(expense_date)

        if parsed_date.isoformat() != expense_date:
            raise ValueError("Invalid date format")

        selected_month = parsed_date.strftime("%Y-%m")

        add_expense(
            amount,
            category,
            description,
            expense_date
        )

        flash(
            "Expense added successfully!",
            "success"
        )

    except (ValueError, TypeError):
        flash(
            "Please enter valid expense details.",
            "error"
        )

    return redirect(
        url_for("dashboard", month=selected_month)
    )


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    selected_month = request.form.get(
        "month", date.today().strftime("%Y-%m")
    )

    if not valid_month(selected_month):
        selected_month = date.today().strftime("%Y-%m")

    delete_expense(expense_id)

    flash(
        "Expense deleted successfully!",
        "success"
    )

    return redirect(
        url_for("dashboard", month=selected_month)
    )


@app.route("/health")
def health():
    return {"status": "healthy", "version": APP_VERSION}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
