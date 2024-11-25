class BudgetManager:
    def __init__(self):
        self.budgets = {}  # Stores budget limits for each category
        self.transactions = []  # Stores transaction history

    def set_budget(self, category, amount):
        """Set a budget limit for a category."""
        if amount <= 0:
            print("Budget amount must be greater than zero.")
            return
        self.budgets[category] = amount
        print(f"Budget for '{category}' set to {amount}.")

    def add_transaction(self, category, amount):
        """Add a transaction and update the budget."""
        if category not in self.budgets:
            print(f"No budget set for category '{category}'. Please set a budget first.")
            return
        if amount <= 0:
            print("Transaction amount must be greater than zero.")
            return
        self.transactions.append({"category": category, "amount": amount})
        print(f"Transaction added: {category} - {amount}")

    def get_budget_status(self, category):
        """Check the remaining budget for a category."""
        if category not in self.budgets:
            print(f"No budget set for category '{category}'.")
            return
        total_spent = sum(t['amount'] for t in self.transactions if t['category'] == category)
        remaining = self.budgets[category] - total_spent
        print(f"Category: {category}\nBudget: {self.budgets[category]}\nSpent: {total_spent}\nRemaining: {remaining}")

    def view_all_budgets(self):
        """View budgets and their status for all categories."""
        if not self.budgets:
            print("No budgets set.")
            return
        print("Budget Summary:")
        for category in self.budgets:
            self.get_budget_status(category)

# Example usage
if __name__ == "__main__":
    manager = BudgetManager()

    # Set budgets
    manager.set_budget("Food", 300)
    manager.set_budget("Rent", 1000)
    manager.set_budget("Entertainment", 150)

    # Add transactions
    manager.add_transaction("Food", 50)
    manager.add_transaction("Food", 100)
    manager.add_transaction("Rent", 950)
    manager.add_transaction("Entertainment", 20)

    # View budget status
    manager.get_budget_status("Food")
    manager.get_budget_status("Rent")
    manager.get_budget_status("Entertainment")

    # View all budgets
    manager.view_all_budgets()
