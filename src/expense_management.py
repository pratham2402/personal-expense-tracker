import csv
from src.utils import get_valid_month_year, read_csv, write_csv, file_exists, is_valid_date
import datetime

EXPENSES_FILE = 'data/expenses.csv'
CATEGORIES_FILE = 'data/categories.csv'

def load_categories():
    """Load categories from CSV file or return default categories."""
    if not file_exists(CATEGORIES_FILE):
        return ['Food', 'Travel', 'Utilities', 'Entertainment', 'Miscellaneous']
    with open(CATEGORIES_FILE, 'r') as file:
        reader = csv.DictReader(file)
        return [row['Category'] for row in csv.DictReader(file)]

def save_categories(categories):
    """Save categories in the CSV file."""
    with open(CATEGORIES_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Category'])
        writer.writeheader()
        for category in categories:
            writer.writerow({'Category':category})

def manage_category():
    """Menu for managing categories"""
    categories = load_categories()
    while True:
        print("\nCategory Management")
        print("1. View Categories")
        print("2. Add Categories")
        print("3. Remove Category")
        print("4. Return To Main Menu")
        choice = int(input("Choose an option: "))
        if choice == 1:
            print("\nCategories")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
        elif choice == 2:
            new_category = input("Enter new category name: ").strip()
            if new_category in categories:
                print("Category already exists.")
            else:
                categories.append(new_category)
                save_categories(categories)
                print(f"Category '{new_category}' added.")
        elif choice == 3:
            print("\nCategories")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
            try:
                to_remove = int(input("Enter the number of category to remove: ")) - 1
                if 0 <= to_remove < len(categories):
                    removed = categories.pop(to_remove)
                    save_categories(categories)
                    print(f"Category '{removed}' removed.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == 4:
            break
        else:
            print("Invalid option. Try again.")

def add_expense():
    categories = load_categories()
    category = input(f"Enter expense category ({','.join(categories)}): ")
    if category not in categories:
        print("Invalid category. Please choose from the list.")
        return
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except:
        print('Enter a valid number.')
        return
  
    # Adding date
    date = datetime.date.today().strftime('%Y-%m-%d')

    # Defining headers
    headers = ['Date', 'Category', 'Amount']

    # Read the existing expenses
    expenses = read_csv(EXPENSES_FILE)
    
    # Write the new expense
    expenses.append({'Date': date, 'Category': category, 'Amount': amount})
    write_csv(EXPENSES_FILE, headers, expenses)

    print(f"Added Expense: {date} - {category} - ₹{amount}")

def display_expenses():
    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    print("\nYour Expenses:")
    print(f"{'Date':<15}{'Category':<15}{'Amount':<10}")
    print("-" * 40)
    for row in expenses:
        print(f"{row['Date']:<15}{row['Category']:<15}₹{row['Amount']:<10}")

def delete_by_index():
    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("All Expenses")
    for i, row in enumerate(expenses, 1):
        print(f"{i}. {row['Category']} - {row['Amount']} (Date: {row['Date']})")
    
    try:
        index = int(input("\nEnter the index of the expense you want to delete: ")) - 1
        if index < 0 or index >= len(expenses):
            print("Invalid index. No expense found.")
            return
    except ValueError:
        print("Invalid index. Please enter a number.")
        return
    
    confirm = input(f"Are you sure you want to delete the expense: {expenses[index]['Category']} - {expenses[index]['Amount']}?: ")
    if confirm.lower() == 'y':
        expenses.pop(index)
        write_csv(EXPENSES_FILE, ['Date', 'Category', 'Amount'], expenses)
        print("Expense deleted successfully.")
    else:
        print("Deletion cancelled.")

def delete_by_category():
    category_to_delete = input("Enter the category to delete(e.g., Food, Travel, etc): ").strip()
    
    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return

    if not any(row['Category'] == category_to_delete for row in expenses):
        print(f"No expenses found for category '{category_to_delete}'")
        return

    expenses = [row for row in expenses if row['Category'] != category_to_delete]
    write_csv(EXPENSES_FILE, ['Date', 'Category', 'Amount'], expenses)
    print(f"All expenses for category '{category_to_delete}' have been deleted.")

def delete_by_month_year():
    input_month, input_year = get_valid_month_year()
    if not is_valid_date(input_year, input_month):
        print("Invalid month/year input. Please try again.")
        return

    expenses = read_csv(EXPENSES_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return

    expenses = [row for row in expenses if row['Date'][5:7] != input_month or row['Date'][:4] != input_year]
    write_csv(EXPENSES_FILE, ['Date', 'Category', 'Amount'], expenses)
    print(f"All expenses for {input_month}/{input_year} have been deleted.")
