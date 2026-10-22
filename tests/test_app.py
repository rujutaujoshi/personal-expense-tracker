
import pytest
import app as expense_app
import database


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a separate temporary database for testing.
    test_database = tmp_path / "test_expenses.db"

    monkeypatch.setattr(
        database, "DATABASE", test_database
    )

    database.init_db()

    expense_app.app.config.update(
        TESTING=True
    )

    with expense_app.app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Expense Dashboard" in response.data


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["version"] == "1.1"


def test_add_expense(client):
    response = client.post("/add", data={
        "amount": "250",
        "category": "Food",
        "description": "Lunch",
        "date": "2026-10-22"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Lunch" in response.data
    assert b"250.00" in response.data


def test_invalid_expense(client):
    response = client.post("/add", data={
        "amount": "-100",
        "category": "Food",
        "description": "Invalid Expense",
        "date": "2026-10-22"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Please enter valid expense details" in response.data

    assert database.get_expenses("2026-10") == []


def test_month_filter(client):
    database.add_expense(
        100, "Food", "October Lunch", "2026-10-22"
    )

    database.add_expense(
        200, "Transport", "September Taxi", "2026-09-15"
    )

    response = client.get("/?month=2026-10")

    assert response.status_code == 200
    assert b"October Lunch" in response.data
    assert b"September Taxi" not in response.data


def test_delete_expense(client):
    database.add_expense(
        300, "Shopping", "Shoes", "2026-10-22"
    )

    expenses = database.get_expenses("2026-10")
    expense_id = expenses[0]["id"]

    response = client.post(
        f"/delete/{expense_id}",
        data={"month": "2026-10"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert database.get_expenses("2026-10") == []
