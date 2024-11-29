import datetime

users = {}
logged_in_users = {}
transactions = []
categories = ["Food", "Transport", "Entertainment", "Utilities"]
budgets = {}

# Helper Functions
def print_boxed(text_lines):
    """Prints text neatly within a box."""
    max_len = max(len(line) for line in text_lines)
    print("+" + "-" * (max_len + 2) + "+")
    for line in text_lines:
        print(f"| {line.ljust(max_len)} |")
    print("+" + "-" * (max_len + 2) + "+")


def register():
    print("\n--- REGISTER ---")
    username = input("Enter username to register: ").strip()
    if username in users:
        print("⚠️  User already exists. Please choose a different username.")
        return
    password = input("Enter password: ").strip()
    users[username] = password
    print(f"✅ User '{username}' registered successfully!")

def login():
    print("\n--- LOGIN ---")
    username = input("Enter username: ").strip()
    if username not in users:
        print("⚠️  User does not exist. Please register first.")
        return None
    password = input("Enter password: ").strip()
    if users[username] != password:
        print("⚠️  Incorrect password.")
        return None
    logged_in_users[username] = True
    print(f"✅ Welcome back, {username}!")
    return username

def logout(username):
    if username in logged_in_users:
        del logged_in_users[username]
        print(f"👋 Goodbye, {username}. You have been logged out.")
    else:
        print("⚠️  You are not logged in.")


def add_transaction(username):
    print("\n--- ADD TRANSACTION ---")
    transaction_type = input("Enter transaction type (income/expense): ").strip().lower()
    if transaction_type not in ["income", "expense"]:
        print("⚠️  Invalid transaction type. Please enter 'income' or 'expense'.")
        return
    try:
        amount = float(input("Enter transaction amount: ").strip())
    except ValueError:
        print("⚠️  Invalid amount. Please enter a numeric value.")
        return
    category = input(f"Enter category {categories}: ").strip()
    if category not in categories:
        print(f"⚠️  Invalid category. Must be one of {categories}.")
        return
    date_input = input("Enter transaction date (YYYY-MM-DD): ").strip()
    try:
        date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("⚠️  Invalid date format. Use YYYY-MM-DD.")
        return

    if transaction_type == "expense" and category in budgets:
        projected_spent = budgets[category]["spent"] + amount
        if projected_spent > budgets[category]["limit"]:
            print(f"⚠️  Budget Alert! You are about to exceed the budget for '{category}'.")
            print(f"Current Spent: ₱{budgets[category]['spent']}, New Total: ₱{projected_spent}, Limit: ₱{budgets[category]['limit']}")
            proceed = input("Do you want to continue with this transaction? (yes/no): ").strip().lower()
            if proceed != "yes":
                print("⚠️  Transaction canceled.")
                return

    transaction = {"username": username, "type": transaction_type, "amount": amount, "category": category, "date": date}
    transactions.append(transaction)
    print("✅ Transaction added successfully!")
    if transaction_type == "expense" and category in budgets:
        budgets[category]["spent"] += amount

def view_transactions(username):
    print("\n--- YOUR TRANSACTIONS ---")
    user_transactions = [t for t in transactions if t["username"] == username]
    if not user_transactions:
        print("📂 No transactions found.")
        return
    print(f"\n📊 Transactions for {username}:")
    print("-" * 50)
    for i, transaction in enumerate(user_transactions, start=1):
        print(f"{i}. Type: {transaction['type'].capitalize()}, Amount: ₱{transaction['amount']:.2f}, "
              f"Category: {transaction['category']}, Date: {transaction['date']}")
    print("-" * 50)

def delete_transaction(username):
    print("\n--- DELETE TRANSACTION ---")
    view_transactions(username)
    if not transactions:
        return
    try:
        transaction_index = int(input(f"Enter the number of the transaction to delete: ")) - 1
        if 0 <= transaction_index < len(transactions):
            deleted_transaction = transactions.pop(transaction_index)
            print(f"✅ Transaction '{deleted_transaction['type'].capitalize()} - ₱{deleted_transaction['amount']}' deleted.")
        else:
            print("⚠️  Invalid transaction number.")
    except ValueError:
        print("⚠️  Please enter a valid number.")

def update_transaction(username):
    print("\n--- UPDATE TRANSACTION ---")
    view_transactions(username)
    if not transactions:
        return
    try:
        transaction_index = int(input(f"Enter the number of the transaction to update: ")) - 1
        if 0 <= transaction_index < len(transactions):
            transaction = transactions[transaction_index]
            print(f"Current details: {transaction}")
            print("What would you like to update?")
            update_choice = input("Type 'amount', 'category', or 'date' to update, or 'cancel' to cancel: ").strip().lower()
            if update_choice == "amount":
                try:
                    new_amount = float(input("Enter the new amount: "))
                    transaction["amount"] = new_amount
                except ValueError:
                    print("⚠️  Invalid amount. Please enter a numeric value.")
            elif update_choice == "category":
                new_category = input(f"Enter the new category {categories}: ").strip()
                if new_category in categories:
                    transaction["category"] = new_category
                else:
                    print(f"⚠️  Invalid category. Choose one from {categories}.")
            elif update_choice == "date":
                new_date_input = input("Enter the new transaction date (YYYY-MM-DD): ").strip()
                try:
                    new_date = datetime.datetime.strptime(new_date_input, "%Y-%m-%d").date()
                    transaction["date"] = new_date
                except ValueError:
                    print("⚠️  Invalid date format. Use YYYY-MM-DD.")
            elif update_choice == "cancel":
                print("⚠️  Update cancelled.")
            else:
                print("⚠️  Invalid choice.")
            print(f"✅ Transaction updated: {transaction}")
        else:
            print("⚠️  Invalid transaction number.")
    except ValueError:
        print("⚠️  Please enter a valid number.")


class BudgetManager:
    def __init__(self):
        self.budgets = {}  # Stores budget limits for each category

    def set_budget(self):
        """Set a budget limit for a category."""
        category = input(f"Enter category {categories}: ").strip()
        if category not in categories:
            print(f"⚠️  Invalid category. Must be one of {categories}.")
            return
        try:
            amount = float(input(f"Enter budget amount for {category}: "))
        except ValueError:
            print("⚠️  Invalid amount. Please enter a numeric value.")
            return
        budgets[category] = {"limit": amount, "spent": 0}
        print(f"✅ Budget for '{category}' set to ₱{amount}.")

    def view_budget_status(self):
        print("\n--- BUDGET STATUS ---")
        if not budgets:
            print("📂 No budgets set.")
            return
        for category, budget in budgets.items():
            remaining = budget["limit"] - budget["spent"]
            print(f"{category.capitalize()}: Limit = ₱{budget['limit']}, Spent = ₱{budget['spent']}, Remaining = ₱{remaining}")
        print("-" * 50)

    def financial_summary(self, username):
        print("\n--- FINANCIAL SUMMARY ---")
        user_transactions = [t for t in transactions if t["username"] == username]
        if not user_transactions:
            print("📂 No transactions found.")
            return
        total_income = sum(t["amount"] for t in user_transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in user_transactions if t["type"] == "expense")
        net_balance = total_income - total_expense
        print(f"Total Income: ₱{total_income:.2f}")
        print(f"Total Expenses: ₱{total_expense:.2f}")
        print(f"Net Balance: ₱{net_balance:.2f}")

        # Show Budget Status per Category
        print("\nCategory Budget Status:")
        for category in categories:
            category_spent = sum(t["amount"] for t in user_transactions if t["category"] == category and t["type"] == "expense")
            if category in budgets:
                remaining_budget = budgets[category]["limit"] - category_spent
                print(f"{category.capitalize()}: Spent = ₱{category_spent:.2f}, Remaining = ₱{remaining_budget:.2f}")
            else:
                print(f"{category.capitalize()}: No budget set.")
        print("-" * 50)

# Main Menu
def main_menu():
    while True:
        print("\n===============================")
        print("🪙    WELCOME TO PENNY WISE!  🪙")
        print("===============================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("===============================")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                logged_in_menu(username)
        elif choice == "3":
            print("👋 Thank you for using Budget Tracker. Goodbye!")
            break
        else:
            print("⚠️  Invalid choice. Please try again.")

def logged_in_menu(username):
    budget_manager = BudgetManager()
    while True:
        print("\n===============================")
        print(f"📌 PENNY WISER BOARD: {username.upper()}")
        print("===============================")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Set Budget")
        print("6. View Budget Status")
        print("7. View Financial Summary")
        print("8. Logout")
        print("===============================")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_transaction(username)
        elif choice == "2":
            view_transactions(username)
        elif choice == "3":
            update_transaction(username)
        elif choice == "4":
            delete_transaction(username)
        elif choice == "5":
            budget_manager.set_budget()
        elif choice == "6":
            budget_manager.view_budget_status()
        elif choice == "7":
            budget_manager.financial_summary(username)
        elif choice == "8":
            logout(username)
            break
        else:
            print("⚠️  Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
