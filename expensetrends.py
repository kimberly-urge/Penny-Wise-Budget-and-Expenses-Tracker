categories = ["Food", "Transport", "Entertainment", "Utilities", "Others"]

expense_trends = {}

def add_expense(category, amount, date):
    if category not in expense_trends:
        expense_trends[category] = []
    expense_trends[category].append({"date": date, "amount": amount})
    print(f"\n✅ Expense added: {category} - {amount} on {date}\n")


def view_expense_trends(category=None):
    if not expense_trends:
        print("\n❌ No expenses recorded yet!\n")
        return

    if category:
        if category in expense_trends:
            print(f"\n📊 Trends for {category}:")
            for i, transaction in enumerate(expense_trends[category], start=1):
                print(f"  {i}. Date: {transaction['date']}, Amount: {transaction['amount']}")
        else:
            print(f"\n❌ No data for category: {category}\n")
    else:
        print("\n📊 All Expense Trends:")
        for cat, transactions in expense_trends.items():
            print(f"\nCategory: {cat}")
            for i, transaction in transactions:
                print(f"  {i}. Date: {transaction['date']}, Amount: {transaction['amount']}")


def menu():
    while True:
        print("\n========= Expense Tracker =========")
        print("1. Add Expense")
        print("2. View Expense Trends")
        print("3. Exit")
        print("===================================")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            print("\n=== Add a New Expense ===")
            print("Available categories:")
            for i, cat in enumerate(categories, start=1):
                print(f"  {i}. {cat}")
            try:
                category_choice = int(input("Select a category by number: ").strip())
                if 1 <= category_choice <= len(categories):
                    category = categories[category_choice - 1]
                else:
                    print("❌ Invalid choice! Please select a valid category.\n")
                    continue
            except ValueError:
                print("❌ Invalid input! Please enter a number.\n")
                continue

            try:
                amount = float(input("Enter amount (e.g., 20.5): ").strip())
            except ValueError:
                print("❌ Invalid amount! Please enter a numeric value.\n")
                continue
            date = input("Enter date (YYYY-MM-DD, e.g., 2024-11-29): ").strip()
            add_expense(category, amount, date)
        elif choice == "2":
            print("\n=== View Expense Trends ===")
            category = input("Enter category to view (leave blank for all): ").strip()
            view_expense_trends(category if category else None)
        elif choice == "3":
            print("\n👋 Goodbye! Thanks for using the Expense Tracker.")
            break
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, or 3.\n")

menu()
