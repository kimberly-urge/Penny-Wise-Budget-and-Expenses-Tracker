import csv
import datetime

users_file = "users.csv"
transactions_file = "transactions.csv"
users = {}
logged_in_users = {}
transactions = []
categories = ["Food", "Transport", "Entertainment", "Utilities"]
budgets = {}

# Helper Functions
def save_users():
    """Save user data to CSV file."""
    with open(users_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])
        for username, password in users.items():
            writer.writerow([username, password])

def load_users():
    """Load user data from CSV file."""
    try:
        with open(users_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users[row["username"]] = row["password"]
    except FileNotFoundError:
        pass

def save_transactions():
    """Save transactions to CSV file."""
    with open(transactions_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "type", "amount", "category", "date"])
        for transaction in transactions:
            writer.writerow([
                transaction["username"],
                transaction["type"],
                transaction["amount"],
                transaction["category"],
                transaction["date"],
            ])

def load_transactions():
    """Load transactions from CSV file."""
    try:
        with open(transactions_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append({
                    "username": row["username"],
                    "type": row["type"],
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "date": datetime.datetime.strptime(row["date"], "%Y-%m-%d").date(),
                })
    except FileNotFoundError:
        pass

def register():
    print("\n--- REGISTER ---")
    username = input("Enter username to register: ").strip()
    if username in users:
        print("⚠️  User already exists. Please choose a different username.")
        return
    password = input("Enter password: ").strip()
    users[username] = password
    save_users()
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

    transaction = {
        "username": username,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "date": date,
    }
    transactions.append(transaction)
    save_transactions()
    print("✅ Transaction added successfully!")

def view_transactions(username):
    print("\n--- YOUR TRANSACTIONS ---")
    user_transactions = [t for t in transactions if t["username"] == username]
    if not user_transactions:
        print("📂 No transactions found.")
        return
    print(f"\n📊 Transactions for {username}:")
    print("-" * 50)
    for i, transaction in enumerate(user_transactions, start=1):
        print(
            f"{i}. Type: {transaction['type'].capitalize()}, Amount: ₱{transaction['amount']:.2f}, "
            f"Category: {transaction['category']}, Date: {transaction['date']}"
        )
    print("-" * 50)

def delete_transaction(username):
    print("\n--- DELETE TRANSACTION ---")
    view_transactions(username)
    user_transactions = [t for t in transactions if t["username"] == username]
    if not user_transactions:
        return
    try:
        transaction_index = int(input(f"Enter the number of the transaction to delete: ")) - 1
        if 0 <= transaction_index < len(user_transactions):
            transaction_to_delete = user_transactions[transaction_index]
            transactions.remove(transaction_to_delete)
            save_transactions()
            print(f"✅ Transaction deleted.")
        else:
            print("⚠️  Invalid transaction number.")
    except ValueError:
        print("⚠️  Please enter a valid number.")

def update_transaction(username):
    print("\n--- UPDATE TRANSACTION ---")
    view_transactions(username)
    user_transactions = [t for t in transactions if t["username"] == username]
    if not user_transactions:
        return
    try:
        transaction_index = int(input(f"Enter the number of the transaction to update: ")) - 1
        if 0 <= transaction_index < len(user_transactions):
            transaction = user_transactions[transaction_index]
            print(f"Current details: {transaction}")
            update_field = input("What would you like to update? (type/amount/category/date): ").strip().lower()
            if update_field == "type":
                transaction["type"] = input("Enter new type (income/expense): ").strip().lower()
            elif update_field == "amount":
                transaction["amount"] = float(input("Enter new amount: ").strip())
            elif update_field == "category":
                transaction["category"] = input(f"Enter new category {categories}: ").strip()
            elif update_field == "date":
                date_input = input("Enter new date (YYYY-MM-DD): ").strip()
                transaction["date"] = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            else:
                print("⚠️  Invalid field.")
                return
            save_transactions()
            print("✅ Transaction updated successfully!")
        else:
            print("⚠️  Invalid transaction number.")
    except ValueError:
        print("⚠️  Please enter a valid number.")

def set_budget():
    print("\n--- SET BUDGET ---")
    category = input(f"Enter category {categories}: ").strip()
    if category not in categories:
        print(f"⚠️  Invalid category. Must be one of {categories}.")
        return
    try:
        limit = float(input(f"Enter budget limit for '{category}': "))
        budgets[category] = {"limit": limit, "spent": 0}
        print(f"✅ Budget for '{category}' set to ₱{limit:.2f}.")
    except ValueError:
        print("⚠️  Invalid amount. Please enter a numeric value.")

def view_budget_status():
    print("\n--- BUDGET STATUS ---")
    if not budgets:
        print("📂 No budgets set.")
        return
    for category, budget in budgets.items():
        spent = sum(
            t["amount"] for t in transactions if t["category"] == category and t["type"] == "expense"
        )
        remaining = budget["limit"] - spent
        print(f"{category.capitalize()}: Limit = ₱{budget['limit']}, Spent = ₱{spent}, Remaining = ₱{remaining:.2f}")
    print("-" * 50)

def financial_summary(username):
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

    print("\nCategory Budget Status:")
    for category in categories:
        category_expenses = sum(
            t["amount"] for t in user_transactions if t["type"] == "expense" and t["category"] == category
        )
        if category in budgets:
            limit = budgets[category]["limit"]
            remaining = max(0, limit - category_expenses)
            print(f"{category.capitalize()}: Spent = ₱{category_expenses:.2f}, Remaining = ₱{remaining:.2f}")
        else:
            print(f"{category.capitalize()}: No budget set.")
    print("-" * 50)

def main_menu():
    load_users()
    load_transactions()
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
            set_budget()
        elif choice == "6":
            view_budget_status()
        elif choice == "7":
            financial_summary(username)
        elif choice == "8":
            logout(username)
            break
        else:
            print("⚠️  Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
