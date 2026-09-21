from expense import Expense
from app import expense_file, sum_expense

TEST_CSV = "test_expense.csv"

# create some test expenses
expenses = [
    Expense("Lunch", 12.5, "🍛Food"),
    Expense("Rent", 1200, "🏠Home"),
    Expense("Subscription", 9.99, "🎫Subscription"),
]

# write them
for e in expenses:
    expense_file(e, TEST_CSV)

# summarize with a budget
sum_expense(TEST_CSV, 2000)
