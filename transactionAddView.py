import csv
from datetime import datetime, timedelta


class RecurringTransactionManager:
    def __init__(self):
        self.recurring_transactions = []  # List to store recurring transaction data
        self.transactions = []  # List to store processed transactions

    def add_recurring_transaction(self):
        """Add a recurring transaction."""
        try:
            trans_type = input("Enter transaction type (income/expense): ").strip().lower()
            if trans_type not in ['income', 'expense']:
                print("Invalid type. Must be 'income' or 'expense'.")
                return

            category = input("Enter category (e.g., Rent, Subscription): ").strip()
            amount = float(input(f"Enter amount for {category}: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            interval = input("Enter interval (daily/weekly/monthly/yearly): ").strip().lower()
            if interval not in ['daily', 'weekly', 'monthly', 'yearly']:
                print("Invalid interval. Must be 'daily', 'weekly', 'monthly', or 'yearly'.")
                return

            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            try:
                next_due = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return

            self.recurring_transactions.append({
                "type": trans_type,
                "category": category,
                "amount": amount,
                "interval": interval,
                "next_due": next_due
            })
            print(f"Recurring transaction for '{category}' added successfully.")
        except ValueError:
            print("Invalid input. Please enter valid numbers for the amount.")

    def process_recurring_transactions(self):
        """Process recurring transactions that are due."""
        current_date = datetime.now().date()
        processed_transactions = []

        for transaction in self.recurring_transactions:
            while transaction["next_due"] <= current_date:
                # Add to processed transactions
                self.transactions.append({
                    "type": transaction["type"],
                    "category": transaction["category"],
                    "amount": transaction["amount"],
                    "date": transaction["next_due"]
                })
                processed_transactions.append({
                    "type": transaction["type"],
                    "category": transaction["category"],
                    "amount": transaction["amount"],
                    "date": transaction["next_due"]
                })

                # Update next due date
                transaction["next_due"] = self.calculate_next_due_date(transaction["next_due"], transaction["interval"])

        if processed_transactions:
            print("\nProcessed Transactions:")
            for trans in processed_transactions:
                print(f"{trans['date']}: {trans['type']} - {trans['category']} (${trans['amount']})")
        else:
            print("No recurring transactions to process today.")

    @staticmethod
    def calculate_next_due_date(current_date, interval):
        """Calculate the next due date based on the interval."""
        if interval == "daily":
            return current_date + timedelta(days=1)
        elif interval == "weekly":
            return current_date + timedelta(weeks=1)
        elif interval == "monthly":
            next_month = current_date.month % 12 + 1
            year_increment = (current_date.month + 1) // 13
            return current_date.replace(month=next_month, year=current_date.year + year_increment)
        elif interval == "yearly":
            return current_date.replace(year=current_date.year + 1)

    def view_recurring_transactions(self):
        """View all recurring transactions."""
        if not self.recurring_transactions:
            print("No recurring transactions set.")
            return
        print("\nRecurring Transactions:")
        for trans in self.recurring_transactions:
            print(f"{trans['type'].capitalize()} - {trans['category']} (${trans['amount']}), "
                  f"Interval: {trans['interval']}, Next Due: {trans['next_due']}")

    def view_processed_transactions(self):
        """View all processed transactions."""
        if not self.transactions:
            print("No transactions processed yet.")
            return
        print("\nProcessed Transactions:")
        for trans in self.transactions:
            print(f"{trans['date']}: {trans['type'].capitalize()} - {trans['category']} (${trans['amount']})")

    def export_transactions(self, filename="transactions.csv"):
        """Export all transactions to a CSV file."""
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Type", "Category", "Amount"])
                for trans in self.transactions:
                    writer.writerow([trans["date"], trans["type"], trans["category"], trans["amount"]])
            print(f"Transactions exported successfully to '{filename}'.")
        except Exception as e:
            print(f"Error exporting transactions: {e}")


def main():
    manager = RecurringTransactionManager()

    while True:
        print("\n--- Recurring Transaction Manager ---")
        print("1. Add Recurring Transaction")
        print("2. Process Recurring Transactions")
        print("3. View Recurring Transactions")
        print("4. View Processed Transactions")
        print("5. Export Processed Transactions")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            manager.add_recurring_transaction()
        elif choice == "2":
            manager.process_recurring_transactions()
        elif choice == "3":
            manager.view_recurring_transactions()
        elif choice == "4":
            manager.view_processed_transactions()
        elif choice == "5":
            manager.export_transactions()
        elif choice == "6":
            print("Exiting Recurring Transaction Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
()
