import csv
from src.utils import read_csv, get_valid_month_year, is_valid_date  # No need for os import
import matplotlib.pyplot as plt

EXPENSES_FILE = 'data/expenses.csv'

def category_summary():
    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    summary = {}
    for row in expenses:
        category = row['Category']
        amount = float(row['Amount'])
        summary[category] = summary.get(category, 0) + amount

    print('\nCategory Summary')
    for category, total in summary.items():
        print(f'{category}: ₹{total}')

def display_monthly_report():
    input_month, input_year = get_valid_month_year()
    if not is_valid_date(input_year, input_month):
        print("Invalid month/year input. Please try again.")
        return

    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return

    total_expenses = 0
    record_found = False

    for row in expenses:
        date = row['Date']
        expense_month = date[5:7]
        expense_year = date[:4]

        if input_month == expense_month and input_year == expense_year:
            total_expenses += float(row['Amount'])
            record_found = True
    
    if record_found:
        print(f'Total Expenses for {input_month}/{input_year}: ₹{total_expenses:.2f}')
    else:
        print(f'No expenses recorded for {input_month}/{input_year}.')

def sort_expenses():
    print("Sort by: 1. Date 2. Category 3. Amount")
    choice = input('Choose: ')
    expenses = read_csv(EXPENSES_FILE)

    if choice == '1':
        expenses.sort(key=lambda x: x['Date'])
    elif choice == '2':
        expenses.sort(key=lambda x: x['Category'])
    elif choice == '3':
        expenses.sort(key=lambda x: x['Amount'])
    
    print("\nSorted Expenses")
    for row in expenses:
        print(f"{row['Date']} - {row['Category']} : ₹{row['Amount']}")

def export_data():
    export_file = input("Enter the name of the file to export data to (e.g., summary.csv): ")
    expenses = read_csv(EXPENSES_FILE)
    with open(export_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Category', 'Amount'])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Data exported to {export_file}.")

def visualize_expenses():
    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    summary = {}
    for row in expenses:
        category = row['Category']
        amount = float(row['Amount'])
        summary[category] = summary.get(category, 0) + amount
    
    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title('Expenses By Category')
    plt.show()

def filter_expenses():
    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    # Filtering expenses by min-max amount (range)
    min_amount = float(input("Enter minimum amount: "))
    max_amount = float(input("Enter maximum amount: "))

    print("\nFiltered Expenses")
    print(f"{'Date':<15}{'Category':<15}{'Amount':<10}")
    print('-' * 40)

    for row in expenses:
        amount = float(row['Amount'])
        if min_amount <= amount <= max_amount:
            print(f"{row['Date']:<15}{row['Category']:<15}₹{row['Amount']:<10}")

def create_backup():
    backup_file = 'backup_expenses.csv'
    expenses = read_csv(EXPENSES_FILE)
    with open(backup_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Category', 'Amount'])
        writer.writeheader()
        writer.writerows(expenses)
    print(f'Backup created successfully: {backup_file}')

def monthly_expense_trends():
    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    trends = {}
    for row in expenses:
        month_year = row['Date'][:7]  # [:7] used to get YYYY-MM
        amount = float(row['Amount'])
        trends[month_year] = trends.get(month_year, 0) + amount
    
    months = list(trends.keys())
    amounts = list(trends.values())

    plt.figure(figsize=(10, 6))
    plt.bar(months, amounts, color='skyblue')
    plt.xlabel('Month-Year')
    plt.ylabel('Total Expenses (₹)')
    plt.title('Monthly Expense Trends')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
