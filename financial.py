import datetime


class BudgetManager:
    def __init__(self):
        """Initialize the Budget Manager with budgets and transactions."""
        self.budgets = {}
        self.transactions = []
        self.CATEGORIES = ["food", "entertainment", "transport", "salary", "miscellaneous"]

    @staticmethod
    def print_boxed(text_lines):
        """Prints text neatly within a box."""
        max_len = max(len(line) for line in text_lines)
        print("+" + "-" * (max_len + 2) + "+")
        for line in text_lines:
            print(f"| {line.ljust(max_len)} |")
        print("+" + "-" * (max_len + 2) + "+")

    def set_budget(self):
        """Set a budget limit for a category."""
        self.print_boxed(["Set a Budget"])
        category = input(f"Enter category {self.CATEGORIES}: ").strip().lower()
        if category not in self.CATEGORIES:
            print(f"Invalid category. Must be one of {self.CATEGORIES}.")
            return

        try:
            amount = float(input(f"Enter the budget amount for {category}: "))
            if amount <= 0:
                print("Budget amount must be greater than zero.")
                return
            self.budgets[category] = {"limit": amount, "spent": 0}
            print(f"Budget for '{category}' set to {amount}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def add_transaction(self):
        """Add a transaction and update the budget."""
        self.print_boxed(["Add a Transaction"])
        t_type = input("Enter type (income/expense): ").strip().lower()
        if t_type not in ['income', 'expense']:
            print("Invalid type. Must be 'income' or 'expense'.")
            return

        try:
            amount = float(input("Enter transaction amount: "))
            if amount <= 0:
                print("Amount must be a positive number.")
                return
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return

        category = input(f"Enter category {self.CATEGORIES}: ").strip().lower()
        if category not in self.CATEGORIES:
            print(f"Invalid category. Must be one of {self.CATEGORIES}.")
            return

        date_input = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return


        transaction = {"type": t_type, "amount": amount, "category": category, "date": date}
        self.transactions.append(transaction)


        if t_type == "expense" and category in self.budgets:
            self.budgets[category]["spent"] += amount

        print("Transaction added successfully!")

    def view_transactions(self):
        """Display all transactions."""
        if not self.transactions:
            self.print_boxed(["No transactions found."])
            return

        lines = ["All Transactions:"]
        for idx, transaction in enumerate(self.transactions, start=1):
            lines.append(f"{idx}. {transaction['type'].capitalize()} - {transaction['amount']} "
                         f"({transaction['category']}) on {transaction['date']}")
        self.print_boxed(lines)

    def view_transactions_by_month(self):
        """Filter and display transactions by a specific month and year."""
        if not self.transactions:
            self.print_boxed(["No transactions found."])
            return

        try:
            month_input = input("Enter the month and year to filter (MM-YYYY): ").strip()
            month_year = datetime.datetime.strptime(month_input, "%m-%Y")
        except ValueError:
            print("Invalid format. Use MM-YYYY.")
            return

        filtered_transactions = [
            t for t in self.transactions
            if t['date'].month == month_year.month and t['date'].year == month_year.year
        ]

        if not filtered_transactions:
            self.print_boxed([f"No transactions found for {month_year.strftime('%B %Y')}."])
            return

        lines = [f"Transactions for {month_year.strftime('%B %Y')}:"]

        for idx, transaction in enumerate(filtered_transactions, start=1):
            lines.append(f"{idx}. {transaction['type'].capitalize()} - {transaction['amount']} "
                         f"({transaction['category']}) on {transaction['date']}")
        self.print_boxed(lines)

    def view_budget_status(self):
        """Check and display the budget status for all categories."""
        if not self.budgets:
            self.print_boxed(["No budgets set."])
            return

        lines = ["Budget Status:"]
        for category, budget in self.budgets.items():
            remaining = budget["limit"] - budget["spent"]
            lines.append(f"{category.capitalize()}: Limit = {budget['limit']}, "
                         f"Spent = {budget['spent']}, Remaining = {remaining}")
        self.print_boxed(lines)

    def delete_transaction(self):
        """Delete a transaction."""
        if not self.transactions:
            self.print_boxed(["No transactions to delete."])
            return

        self.view_transactions()

        try:
            transaction_index = int(input("Enter the transaction number to delete: ")) - 1
            if transaction_index < 0 or transaction_index >= len(self.transactions):
                print("Invalid transaction number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid transaction number.")
            return

        # Confirm deletion
        transaction = self.transactions[transaction_index]
        confirm = input(f"Are you sure you want to delete this transaction? (yes/no): ").strip().lower()
        if confirm == "yes":
            del self.transactions[transaction_index]
            print("Transaction deleted successfully!")
        else:
            print("Transaction not deleted.")

    def update_transaction(self):
        """Update a specific transaction."""
        if not self.transactions:
            self.print_boxed(["No transactions to update."])
            return

        self.view_transactions()

        try:
            transaction_index = int(input("Enter the transaction number to update: ")) - 1
            if transaction_index < 0 or transaction_index >= len(self.transactions):
                print("Invalid transaction number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid transaction number.")
            return

        transaction = self.transactions[transaction_index]
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

        category = input(f"Enter category {self.CATEGORIES} [{transaction['category']}]: ").strip().lower()
        if category and category not in self.CATEGORIES:
            print(f"Invalid category. Must be one of {self.CATEGORIES}.")
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

    def calculate_financial_summary(self):
        """Calculate total income, expenses, and remaining budget for each category."""
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')


        category_summary = []
        for category, budget in self.budgets.items():
            remaining = budget["limit"] - budget["spent"]
            category_summary.append(
                f"{category.capitalize()}: Limit = {budget['limit']}, "
                f"Spent = {budget['spent']}, Remaining = {remaining}"
            )

        return total_income, total_expenses, category_summary

    def view_financial_summary(self):
        """Display the financial summary."""
        if not self.transactions:
            self.print_boxed(["No transactions found."])
            return

        total_income, total_expenses, category_summary = self.calculate_financial_summary()

        lines = [
            "Financial Summary:",
            f"Total Income: {total_income}",
            f"Total Expenses: {total_expenses}",
            "Category-wise Budget Status:",
        ] + category_summary
        self.print_boxed(lines)


def main():
    manager = BudgetManager()

    while True:
        manager.print_boxed([
            "Transaction & Budget Manager",
            "1. Add a Transaction",
            "2. View Transactions",
            "3. View Transactions by Month",
            "4. Update a Transaction",
            "5. Delete a Transaction",
            "6. Set a Budget",
            "7. View Budget Status",
            "8. View Financial Summary",
            "9. Exit"
        ])

        choice = input("Choose an option: ").strip()
        if choice == "1":
            manager.add_transaction()
        elif choice == "2":
            manager.view_transactions()
        elif choice == "3":
            manager.view_transactions_by_month()
        elif choice == "4":
            manager.update_transaction()
        elif choice == "5":
            manager.delete_transaction()
        elif choice == "6":
            manager.set_budget()
        elif choice == "7":
            manager.view_budget_status()
        elif choice == "8":
            manager.view_financial_summary()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
