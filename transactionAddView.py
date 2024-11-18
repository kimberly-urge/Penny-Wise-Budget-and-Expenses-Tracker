import datetime

# List for the transactions
transactions = []

CATEGORIES = ["food", "entertainment", "transport", "salary", "miscellaneous"]

def print_boxed(text_lines):
    """Prints text neatly within a box."""
    max_len = max(len(line) for line in text_lines)
    print("+" + "-" * (max_len + 2) + "+")
    for line in text_lines:
        print(f"| {line.ljust(max_len)} |")
    print("+" + "-" * (max_len + 2) + "+")

def add_transaction():
    print_boxed(["Add a Transaction"])
    t_type = input("Enter type (income/expense): ").strip().lower()
    if t_type not in ['income', 'expense']:
        print("Invalid type. Must be 'income' or 'expense'.")
        return

    try:
        amount = float(input("Enter amount: ").strip())
        if amount <= 0:
            print("Amount must be a positive number.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input(f"Enter category {CATEGORIES}: ").strip().lower()
    if category not in CATEGORIES:
        print(f"Invalid category. Must be one of {CATEGORIES}.")
        return

    date_input = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    # Store the transaction
    transaction = {
        "type": t_type,
        "amount": amount,
        "category": category,
        "date": date
    }
    transactions.append(transaction)
    print("Transaction added successfully!")

def view_transactions():
    if not transactions:
        print_boxed(["No transactions found."])
        return

    lines = ["All Transactions:"]
    for idx, transaction in enumerate(transactions, start=1):
        lines.append(f"{idx}. {transaction['type'].capitalize()} - {transaction['amount']} ({transaction['category']}) on {transaction['date']}")
    print_boxed(lines)

def view_transactions_by_month():
    if not transactions:
        print_boxed(["No transactions found."])
        return

    try:
        month_input = input("Enter the month and year to filter (MM-YYYY): ").strip()
        month_year = datetime.datetime.strptime(month_input, "%m-%Y")
    except ValueError:
        print("Invalid format. Use MM-YYYY.")
        return

    filtered_transactions = [
        t for t in transactions
        if t['date'].month == month_year.month and t['date'].year == month_year.year
    ]

    if not filtered_transactions:
        print_boxed([f"No transactions found for {month_year.strftime('%B %Y')}."])
        return

    lines = [f"Transactions for {month_year.strftime('%B %Y')}:"]

    for idx, transaction in enumerate(filtered_transactions, start=1):
        lines.append(f"{idx}. {transaction['type'].capitalize()} - {transaction['amount']} ({transaction['category']}) on {transaction['date']}")
    print_boxed(lines)

def update_transaction():
    if not transactions:
        print_boxed(["No transactions to update."])
        return

    view_transactions()  # Display transactions to select from
    try:
        transaction_index = int(input("Enter the transaction number to update: ")) - 1
        if transaction_index < 0 or transaction_index >= len(transactions):
            print("Invalid transaction number.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid transaction number.")
        return

    transaction = transactions[transaction_index]

    print("Leave fields blank to keep the current value.")

    t_type = input(f"Enter type (income/expense) [{transaction['type']}]: ").strip().lower()
    if t_type and t_type not in ['income', 'expense']:
        print("Invalid type. Must be 'income' or 'expense'.")
        return
    transaction['type'] = t_type if t_type else transaction['type']

    amount_input = input(f"Enter amount [{transaction['amount']}]: ").strip()
    if amount_input:
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be a positive number.")
                return
            transaction['amount'] = amount
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

    category = input(f"Enter category {CATEGORIES} [{transaction['category']}]: ").strip().lower()
    if category and category not in CATEGORIES:
        print(f"Invalid category. Must be one of {CATEGORIES}.")
        return
    transaction['category'] = category if category else transaction['category']

    date_input = input(f"Enter date (YYYY-MM-DD) [{transaction['date']}]: ").strip()
    if date_input:
        try:
            date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            transaction['date'] = date
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

    print("Transaction updated successfully!")

def delete_transaction():
    if not transactions:
        print_boxed(["No transactions to delete."])
        return

    view_transactions()  # Display transactions to select from
    try:
        transaction_index = int(input("Enter the transaction number to delete: ")) - 1
        if transaction_index < 0 or transaction_index >= len(transactions):
            print("Invalid transaction number.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid transaction number.")
        return

    # Confirm deletion
    transaction = transactions[transaction_index]
    confirm = input(f"Are you sure you want to delete this transaction? (yes/no): ").strip().lower()
    if confirm == "yes":
        del transactions[transaction_index]
        print("Transaction deleted successfully!")
    else:
        print("Transaction not deleted.")

def main():
    while True:
        print_boxed([
            "Transaction Tracker",
            "1. Add a Transaction",
            "2. View Transactions",
            "3. View Transactions by Month",
            "4. Update a Transaction",
            "5. Delete a Transaction",
            "6. Exit"
        ])

        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            view_transactions_by_month()
        elif choice == "4":
            update_transaction()
        elif choice == "5":
            delete_transaction()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
