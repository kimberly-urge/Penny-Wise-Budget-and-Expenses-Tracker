import pytest
import datetime

# Core data structures for the budget tracker
@pytest.fixture(autouse=True)
def setup():
    global users, logged_in_users, transactions, budgets
    users = {}
    logged_in_users = {}
    transactions = []
    budgets = {}

def test_register_user():
    username = "testuser"
    password = "password123"

    assert username not in users
    users[username] = password
    assert username in users
    assert users[username] == password

def test_login_user():
    username = "testuser"
    password = "password123"
    users[username] = password

    assert username not in logged_in_users
    if username in users and users[username] == password:
        logged_in_users[username] = True
    assert username in logged_in_users

def test_add_transaction():
    username = "testuser"
    users[username] = "password123"
    logged_in_users[username] = True
    transaction_type = "expense"
    amount = 50.0
    category = "Food"
    date = datetime.date.today()

    assert len(transactions) == 0
    transaction = {
        "username": username,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "date": date,
    }
    transactions.append(transaction)
    assert len(transactions) == 1
    assert transactions[0] == transaction

def test_set_budget():
    category = "Food"
    limit = 200.0

    assert category not in budgets
    budgets[category] = {"limit": limit, "spent": 0}
    assert category in budgets
    assert budgets[category] == {"limit": limit, "spent": 0}

def test_view_budget_status():
    category = "Food"
    budgets[category] = {"limit": 200.0, "spent": 50.0}

    assert category in budgets
    remaining = budgets[category]["limit"] - budgets[category]["spent"]
    assert remaining == 150.0

def test_financial_summary():
    username = "testuser"
    users[username] = "password123"
    logged_in_users[username] = True

    transactions.extend([
        {"username": username, "type": "income", "amount": 1000.0, "category": "Food", "date": datetime.date.today()},
        {"username": username, "type": "expense", "amount": 200.0, "category": "Food", "date": datetime.date.today()},
    ])

    total_income = sum(t["amount"] for t in transactions if t["type"] == "income" and t["username"] == username)
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense" and t["username"] == username)
    net_balance = total_income - total_expense

    assert total_income == 1000.0
    assert total_expense == 200.0
    assert net_balance == 800.0
def delete_transaction(transactions, transaction_index):
    transactions.pop(transaction_index)


def update_transaction(transactions, transaction_index, updated_transaction):
    transactions[transaction_index] = updated_transaction


def test_delete_transaction():
    username = "testuser"
    users[username] = "password123"
    logged_in_users[username] = True
    transaction_type = "expense"
    amount = 50.0
    category = "Food"
    date = datetime.date.today()

    # Create a transaction
    transaction = {
        "username": username,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "date": date,
    }
    transactions.append(transaction)
    assert len(transactions) == 1

    # Delete the transaction
    delete_transaction(transactions, 0)
    assert len(transactions) == 0


def test_update_transaction():
    username = "testuser"
    users[username] = "password123"
    logged_in_users[username] = True
    transaction_type = "expense"
    amount = 50.0
    category = "Food"
    date = datetime.date.today()

    # Create a transaction
    transaction = {
        "username": username,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "date": date,
    }
    transactions.append(transaction)
    assert len(transactions) == 1

    # Update the transaction
    updated_amount = 75.0
    updated_category = "Transportation"
    updated_transaction = {
        "username": username,
        "type": transaction_type,
        "amount": updated_amount,
        "category": updated_category,
        "date": date,
    }
    update_transaction(transactions, 0, updated_transaction)
    assert len(transactions) == 1
    assert transactions[0] == updated_transaction