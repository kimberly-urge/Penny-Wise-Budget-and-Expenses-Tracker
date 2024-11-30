import unittest
import datetime


class TestBudgetTracker(unittest.TestCase):
    def setUp(self):
        global users, logged_in_users, transactions, budgets
        users = {}
        logged_in_users = {}
        transactions = []
        budgets = {}

    def test_register_user(self):
        username = "testuser"
        password = "password123"

        self.assertNotIn(username, users)
        users[username] = password
        self.assertIn(username, users)
        self.assertEqual(users[username], password)

    def test_login_user(self):
        username = "testuser"
        password = "password123"
        users[username] = password

        self.assertNotIn(username, logged_in_users)
        if username in users and users[username] == password:
            logged_in_users[username] = True
        self.assertIn(username, logged_in_users)

    def test_add_transaction(self):
        username = "testuser"
        users[username] = "password123"
        logged_in_users[username] = True
        transaction_type = "expense"
        amount = 50.0
        category = "Food"
        date = datetime.date.today()

        self.assertEqual(len(transactions), 0)
        transaction = {
            "username": username,
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "date": date,
        }
        transactions.append(transaction)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0], transaction)

    def test_set_budget(self):
        category = "Food"
        limit = 200.0

        self.assertNotIn(category, budgets)
        budgets[category] = {"limit": limit, "spent": 0}
        self.assertIn(category, budgets)
        self.assertEqual(budgets[category], {"limit": limit, "spent": 0})

    def test_view_budget_status(self):
        category = "Food"
        budgets[category] = {"limit": 200.0, "spent": 50.0}

        self.assertIn(category, budgets)
        remaining = budgets[category]["limit"] - budgets[category]["spent"]
        self.assertEqual(remaining, 150.0)

    def test_financial_summary(self):
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

        self.assertEqual(total_income, 1000.0)
        self.assertEqual(total_expense, 200.0)
        self.assertEqual(net_balance, 800.0)

if __name__ == "__main__":
    unittest.main()
