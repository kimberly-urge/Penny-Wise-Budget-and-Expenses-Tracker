import csv
from datetime import datetime, timedelta
from collections import defaultdict


class PennyWise:
    def __init__(self):
        self.transactions = []  # List of all transactions
        self.trends = defaultdict(list)  # Dictionary to store trends by category
        self.budgets = {}  # Dictionary to store budgets by category

    def set_budget(self):
        """Set a budget for a category."""
        category = input("Enter the category name: ").strip()
        try:
            budget = float(input(f"Enter the budget amount for {category}: "))
            if budget <= 0:
                print("Budget amount must be greater than zero.")
                return
            self.budgets[category] = budget
            print(f"Budget for '{category}' set to ${budget}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def add_transaction(self):
        """Add a transaction and update the trends."""
        try:
            category = input("Enter category (e.g., Food, Rent): ").strip()
            amount = float(input(f"Enter amount for {category}: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            date_str = input("Enter transaction date (YYYY-MM-DD) or leave blank for today: ").strip()
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")
                    return
            else:
                date = datetime.now().date()

            transaction = {"category": category, "amount": amount, "date": date}
            self.transactions.append(transaction)
            self.trends[category].append(transaction)

            # Check against the budget
            if category in self.budgets:
                total_spent = sum(t['amount'] for t in self.trends[category])
                if total_spent > self.budgets[category]:
                    print(f"Warning: You have exceeded the budget for '{category}'!")
            print(f"Transaction added: {category} - ${amount} on {date}.")
        except ValueError:
            print("Invalid input. Please enter a valid number for the amount.")

    def analyze_trends(self):
        """Analyze spending trends and provide advice."""
        print("\n--- Spending Analysis ---")
        for category, transactions in self.trends.items():
            total_spent = sum(t['amount'] for t in transactions)
            budget = self.budgets.get(category, "No budget set")
            print(f"Category: {category}")
            print(f"  Total Spent: ${total_spent}")
            print(f"  Budget: {budget if isinstance(budget, str) else f'${budget}'}")
            if isinstance(budget, (int, float)) and total_spent > budget:
                print("  Advice: You're overspending in this category. Consider reducing unnecessary expenses.")
            elif isinstance(budget, (int, float)):
                print("  Advice: Good job staying within budget! Keep it up.")
            else:
                print("  Advice: Consider setting a budget for this category.")

    def view_trends(self):
        """View spending trends grouped by intervals."""
        category = input("Enter category to view trends: ").strip()
        if category not in self.trends:
            print(f"No transactions found for category '{category}'.")
            return

        interval = input("Enter grouping interval (daily/weekly/monthly): ").strip().lower()
        if interval not in ['daily', 'weekly', 'monthly']:
            print("Invalid interval. Must be 'daily', 'weekly', or 'monthly'.")
            return

        grouped_trends = defaultdict(float)
        for trans in self.trends[category]:
            if interval == "daily":
                key = trans["date"]
            elif interval == "weekly":
                key = trans["date"] - timedelta(days=trans["date"].weekday())  # Start of the week
            elif interval == "monthly":
                key = trans["date"].replace(day=1)  # First day of the month

            grouped_trends[key] += trans["amount"]

        print(f"\nTrends for '{category}' grouped by {interval}:")
        for key, total in sorted(grouped_trends.items()):
            print(f"{key}: ${total}")

    def export_data(self, filename="pennywise_data.csv"):
        """Export transactions and trends data to a CSV file."""
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Category", "Date", "Amount"])
                for transaction in self.transactions:
                    writer.writerow([transaction["category"], transaction["date"], transaction["amount"]])
            print(f"Data exported successfully to '{filename}'.")
        except Exception as e:
            print(f"Error exporting data: {e}")


def main():
    manager = PennyWise()

    while True:
        print("\n--- Welcome to Penny Wise ---")
        print("1. Set Budget for a Category")
        print("2. Add Transaction")
        print("3. Analyze Spending Trends")
        print("4. View Trends by Timeframe")
        print("5. Export Data to CSV")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            manager.set_budget()
        elif choice == "2":
            manager.add_transaction()
        elif choice == "3":
            manager.analyze_trends()
        elif choice == "4":
            manager.view_trends()
        elif choice == "5":
            manager.export_data()
        elif choice == "6":
            print("Thank you for using Penny Wise. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
