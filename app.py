from expense import Expense
import calendar
import datetime
import csv
import os

def main():
    print(f"Running Expense-Tracker!!")
    expense_file_path = "expense.csv"
    budget = 2000

    expense = user_expense()

    expense_file(expense, expense_file_path)

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
    write_header = not os.path.exists(expense_file_path) or os.path.getsize(expense_file_path) == 0
    with open(expense_file_path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["name", "amount", "category"])
        writer.writerow([expense.name, f"{expense.amount}", expense.category])


def sum_expense(expense_file_path, budget):
    print(f"Summarizing User Expense")
    expenses: list[Expense] = []
    if not os.path.exists(expense_file_path):
        print(f"No expense file found at {expense_file_path}. Nothing to summarize.")
        return

    with open(expense_file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or not row.get("name"):
                continue
            try:
                expense_name = row.get("name")
                expense_amount = float(row.get("amount", 0))
                expense_category = row.get("category", "")
            except ValueError:
                print("Skipping malformed row:", row)
                continue

            print(expense_name, expense_amount, expense_category)
            line_expense = Expense(name=expense_name, amount=float(expense_amount), category=expense_category)
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

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    print("Remaining days of the month is ", remaining_days)
    if remaining_days <= 0:
        print("No remaining days in this month.")
        daily_budget = 0.0
    elif remaining_budget <= 0:
        print("You've exceeded your budget.")
        daily_budget = 0.0
    else:
        daily_budget = remaining_budget / remaining_days

    print(f"Budget per day: ${daily_budget:.2f}")


if __name__=="__main__":
    main()