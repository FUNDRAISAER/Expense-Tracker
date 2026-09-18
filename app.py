from expense import Expense
import calendar
import datetime

def main():
    print(f"Running Expense-Tracker!!")
    expense_file_path = "expense.csv"
    budget = 2000

    expense = user_expense()

    #expense_file(expense, expense_file_path)

    sum_expense(expense_file_path, budget)

def user_expense():
    print("🔍Getting user expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍛Food",
        "🏠Home", 
        "👷🏽Work", 
        "🎫Subscription", 
        "✨misc"
    ]

    while True:
        print("Select a category")
        for i, category_name in enumerate(expense_categories):
            print(f"{i+1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: "))-1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, amount=expense_amount, category=selected_category)
            return new_expense
        else:
            print("Invalid category.Please try again!")


def expense_file(expense: Expense, expense_file_path):
    print(f"Saving user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def sum_expense(expense_file_path, budget):
    print(f"Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            print(expense_name, expense_amount, expense_category)
            line_expense = Expense(
                name=expense_name, amount=float(expense_amount), category=expense_category
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category: ")
    for key, amount in amount_by_category.items():
        print(f"   {key}: ${amount:.2f}")

    total_spent = sum(e.amount for e in expenses)
    print(f"You've spent ${total_spent:.2f} this month!")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining: ${remaining_budget:.2f}")

if __name__=="__main__":
    main()