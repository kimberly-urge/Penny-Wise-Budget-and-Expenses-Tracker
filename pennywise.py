import csv
import datetime

users_file = "users.csv"
transactions_file = "transactions.csv"
users = {}
logged_in_users = {}
transactions = []
categories = ["Food", "Transport", "Entertainment", "Utilities"]
budgets = {}
user_balances = {}
user_income_periods = {}

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
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("⚠️  Amount must be a positive number.")
        return

    if transaction_type == "income":
        period = input("Enter period (week/month): ").strip().lower()
        if period not in ["week", "month"]:
            print("⚠️  Invalid period. Please enter 'week' or 'month'.")
            return
        try:
            start_date = datetime.datetime.strptime(input("Enter start date (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
        except ValueError:
            print("⚠️  Invalid date format. Use YYYY-MM-DD.")
            return
        user_balances[username] = user_balances.get(username, 0) + amount
        user_income_periods[username] = {"start_date": start_date, "period_type": period}
        transactions.append({
            "username": username,
            "type": "income",
            "amount": amount,
            "category": "Income",  # Default category for income
            "date": datetime.date.today(),
        })
        save_transactions()
        print(f"✅ Income added. Balance: ₱{user_balances[username]:.2f}")

    elif transaction_type == "expense":
        if user_balances.get(username, 0) <= 0:
            print("⚠️  No balance available. Add income first.")
            return
        
        try:
            date = datetime.datetime.strptime(input("Enter transaction date (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
        except ValueError:
            print("⚠️  Invalid date format. Use YYYY-MM-DD.")
            return

        # Allow user to input a custom category or select from suggestions
        print(f"Suggested categories: {', '.join(categories)}")
        category = input(f"Enter category (or press Enter to use custom category): ").strip()

        # If the category is not in the suggested categories, it's considered a custom category
        if category and category not in categories:
            print(f"✅ Custom category '{category}' selected.")
        elif category in categories:
            print(f"✅ Category '{category}' selected.")
        else:
            print("⚠️  Invalid category. Choose from the list or input a custom category.")
            return
        
        if amount > user_balances[username]:
            print("⚠️  Insufficient balance.")
            return
        
        user_balances[username] -= amount
        transactions.append({
            "username": username,
            "type": "expense",
            "amount": amount,
            "category": category if category else "Uncategorized",  # Use custom or default category
            "date": date,
        })
        save_transactions()
        print(f"✅ Expense recorded. Remaining balance: ₱{user_balances[username]:.2f}")



def view_transactions(username):
    print("\n--- VIEW TRANSACTIONS ---")
    user_transactions = [t for t in transactions if t["username"] == username]
    if not user_transactions:
        print("📂 No transactions found.")
        return

    # Get user's income and period
    total_income = sum(t["amount"] for t in user_transactions if t["type"] == "income")
    income_period = user_income_periods.get(username, None)
    
    remaining_balance = 0
    if income_period:
        period_type = income_period["period_type"]
        start_date = income_period["start_date"]
        # Calculate how much time has passed since the income was set
        today = datetime.date.today()
        if period_type == "month":
            # Calculate remaining balance for the month
            days_in_month = (today.replace(day=28) + datetime.timedelta(days=4)).day  # Get number of days in current month
            remaining_days = max(0, days_in_month - today.day)
        elif period_type == "week":
            # Calculate remaining balance for the week
            days_in_week = 7
            remaining_days = max(0, (start_date + datetime.timedelta(days=days_in_week)).day - today.day)
        
        # Calculate remaining balance for that period
        remaining_balance = total_income - sum(t["amount"] for t in user_transactions if t["type"] == "expense")
        period_remaining_text = f"Remaining balance for this {period_type.capitalize()}: ₱{remaining_balance:.2f}"
    else:
        period_remaining_text = "No income set for this period."

    # Sort transactions by date (latest first)
    user_transactions.sort(key=lambda x: x["date"], reverse=True)

    # Ask user how many transactions to load
    try:
        limit_options = [5, 10, 15, 20]
        print(f"Available options: {limit_options}")
        limit = int(input("How many transactions do you want to load? (5/10/15/20): ").strip())
        if limit not in limit_options:
            print("⚠️ Invalid option. Defaulting to 5 transactions.")
            limit = 5
    except ValueError:
        print("⚠️ Invalid input. Defaulting to 5 transactions.")
        limit = 5

    # Select the most recent transactions based on the limit
    displayed_transactions = user_transactions[:limit]

    # Print period remaining balance and table header
    print(f"\n{period_remaining_text}")
    print("+----+----------+----------+----------+------------+")
    print("| #  | Type     | Amount   | Category | Date       |")
    print("+----+----------+----------+----------+------------+")

    # Print each transaction
    for i, t in enumerate(displayed_transactions, start=1):
        print(
            f"| {i:<2} | {t['type'].capitalize():<8} | ₱{t['amount']:<7.2f} | "
            f"{t['category']:<8} | {t['date']} |"
        )

    # Print table footer
    print("+----+----------+----------+----------+------------+")


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
        print(f"{category}: ₱{category_expenses:.2f}")

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
