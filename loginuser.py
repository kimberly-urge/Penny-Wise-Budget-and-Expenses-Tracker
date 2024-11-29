# Data structures
users = {}
logged_in_users = {}
transactions = []

# Function to register a new user
def register():
    print("\n--- REGISTER ---")
    username = input("Enter username to register: ").strip()
    if username in users:
        print("⚠️  User already exists. Please choose a different username.")
        return
    password = input("Enter password: ").strip()
    users[username] = password
    print(f"✅ User '{username}' registered successfully!")


# Function to log in a user
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


# Function to log out a user
def logout(username):
    if username in logged_in_users:
        del logged_in_users[username]
        print(f"👋 Goodbye, {username}. You have been logged out.")
    else:
        print("⚠️  You are not logged in.")


# Function to add a transaction
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
    category = input("Enter transaction category: ").strip()
    date = input("Enter transaction date (YYYY-MM-DD): ").strip()
    transaction = {
        "username": username,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "date": date
    }
    transactions.append(transaction)
    print("✅ Transaction added successfully!")


# Function to view a user's transactions
def view_transactions(username):
    print("\n--- YOUR TRANSACTIONS ---")
    user_transactions = [t for t in transactions if t["username"] == username]
    if not user_transactions:
        print("📂 No transactions found.")
        return
    print(f"\n📊 Transactions for {username}:")
    print("-" * 50)
    for i, transaction in enumerate(user_transactions, start=1):
        print(f"{i}. Type: {transaction['type'].capitalize()}, Amount: {transaction['amount']}, "
              f"Category: {transaction['category']}, Date: {transaction['date']}")
    print("-" * 50)


# Main application function
def main():
    while True:
        print("\n===============================")
        print("🪙  WELCOME TO PENNY WISE  🪙")
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
            print("👋 Thank you for using Penny Wise. Goodbye!")
            break
        else:
            print("⚠️  Invalid choice. Please try again.")


# Logged-in user's menu
def logged_in_menu(username):
    while True:
        print(f"\n===============================")
        print(f"📌 DASHBOARD: {username.upper()}")
        print("===============================")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Logout")
        print("===============================")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_transaction(username)
        elif choice == "2":
            view_transactions(username)
        elif choice == "3":
            logout(username)
            break
        else:
            print("⚠️  Invalid choice. Please try again.")


# Entry point
if __name__ == "__main__":
    main()
