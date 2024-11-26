from utils import fetch_all, execute_query, get_valid_month_year, is_valid_date
import matplotlib.pyplot as plt
import csv 

def category_summary():
    expenses = fetch_all("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print('\nCategory Summary')
    for category, total in expenses:
        print(f'{category}: ₹{total:.2f}')

def display_monthly_report():
    input_month, input_year = get_valid_month_year()
    if not is_valid_date(input_year, input_month):
        print("Invalid month/year input. Please try again.")
        return

    expenses = fetch_all(
        "SELECT SUM(amount) FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", 
        (input_month, input_year)
    )
    total_expenses = expenses[0][0] if expenses[0][0] is not None else 0

    if total_expenses > 0:
        print(f'Total Expenses for {input_month}/{input_year}: ₹{total_expenses:.2f}')
    else:
        print(f'No expenses recorded for {input_month}/{input_year}.')

def sort_expenses():
    print("Sort by: 1. Date 2. Category 3. Amount")
    choice = input('Choose: ')

    if choice == '1':
        expenses = fetch_all("SELECT date, category, amount FROM expenses ORDER BY date")
    elif choice == '2':
        expenses = fetch_all("SELECT date, category, amount FROM expenses ORDER BY category")
    elif choice == '3':
        expenses = fetch_all("SELECT date, category, amount FROM expenses ORDER BY amount")
    else:
        print("Invalid choice. No sorting applied.")
        return

    print("\nSorted Expenses")
    for date, category, amount in expenses:
        print(f"{date} - {category} : ₹{amount:.2f}")

def export_data():
    export_file = input("Enter the name of the file to export data to (e.g., summary.csv): ")
    expenses = fetch_all("SELECT date, category, amount FROM expenses")

    with open(export_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Category', 'Amount'])
        writer.writeheader()
        writer.writerows([{'Date': date, 'Category': category, 'Amount': amount} for date, category, amount in expenses])
    
    print(f"Data exported to {export_file}.")

def visualize_expenses():
    expenses = fetch_all("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    categories = [row[0] for row in expenses]
    amounts = [row[1] for row in expenses]

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title('Expenses By Category')
    plt.show()

def filter_expenses():
    min_amount = float(input("Enter minimum amount: "))
    max_amount = float(input("Enter maximum amount: "))

    expenses = fetch_all(
        "SELECT date, category, amount FROM expenses WHERE amount BETWEEN ? AND ?", 
        (min_amount, max_amount)
    )
    if not expenses:
        print("No expenses found in the specified range.")
        return

    print("\nFiltered Expenses")
    print(f"{'Date':<15}{'Category':<15}{'Amount':<10}")
    print('-' * 40)
    for date, category, amount in expenses:
        print(f"{date:<15}{category:<15}₹{amount:.2f}")

def create_backup():
    backup_file = 'backup_expenses.csv'
    expenses = fetch_all("SELECT date, category, amount FROM expenses")

    with open(backup_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Category', 'Amount'])
        writer.writeheader()
        writer.writerows([{'Date': date, 'Category': category, 'Amount': amount} for date, category, amount in expenses])
    
    print(f'Backup created successfully: {backup_file}')

def monthly_expense_trends():
    expenses = fetch_all(
        "SELECT strftime('%Y-%m', date) AS month_year, SUM(amount) FROM expenses GROUP BY month_year"
    )
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    months = [row[0] for row in expenses]
    amounts = [row[1] for row in expenses]

    plt.figure(figsize=(10, 6))
    plt.bar(months, amounts, color='skyblue')
    plt.xlabel('Month-Year')
    plt.ylabel('Total Expenses (₹)')
    plt.title('Monthly Expense Trends')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
