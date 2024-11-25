class BudgetManager:
    def __init__(self):
        self.budgets = {}  # Stores budget limits for each category
        self.transactions = []  # Stores transaction history

    def set_budget(self):
        """Set a budget limit for a category."""
        category = input("Enter the category name: ")
        try:
            amount = float(input(f"Enter the budget amount for {category}: "))
            if amount <= 0:
                print("Budget amount must be greater than zero.")
                return
            self.budgets[category] = amount
            print(f"Budget for '{category}' set to {amount}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def add_transaction(self):
        """Add a transaction and update the budget."""
        category = input("Enter the category for the transaction: ")
        if category not in self.budgets:
            print(f"No budget set for category '{category}'. Please set a budget first.")
            return
        try:
            amount = float(input(f"Enter the transaction amount for {category}: "))
            if amount <= 0:
                print("Transaction amount must be greater than zero.")
                return
            self.transactions.append({"category": category, "amount": amount})
            print(f"Transaction added: {category} - {amount}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def get_budget_status(self):
        """Check the remaining budget for a category."""
        category = input("Enter the category to check the budget status: ")
        if category not in self.budgets:
            print(f"No budget set for category '{category}'.")
            return
        total_spent = sum(t['amount'] for t in self.transactions if t['category'] == category)
        remaining = self.budgets[category] - total_spent
        print(f"\nCategory: {category}\nBudget: {self.budgets[category]}\nSpent: {total_spent}\nRemaining: {remaining}\n")

    def view_all_budgets(self):
        """View budgets and their status for all categories."""
        if not self.budgets:
            print("No budgets set.")
            return
        print("\nBudget Summary:")
        for category in self.budgets:
            total_spent = sum(t['amount'] for t in self.transactions if t['category'] == category)
            remaining = self.budgets[category] - total_spent
            print(f"Category: {category}\nBudget: {self.budgets[category]}\nSpent: {total_spent}\nRemaining: {remaining}\n")


def main():
    manager = BudgetManager()

    while True:
        print("\n--- Budget Manager ---")
        print("1. Set Budget")
        print("2. Add Transaction")
        print("3. Check Budget Status")
        print("4. View All Budgets")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            manager.set_budget()
        elif choice == "2":
            manager.add_transaction()
        elif choice == "3":
            manager.get_budget_status()
        elif choice == "4":
            manager.view_all_budgets()
        elif choice == "5":
            print("Exiting Budget Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main
