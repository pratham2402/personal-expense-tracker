from utils import get_valid_month_year, is_valid_date, fetch_all, execute_query
import datetime

EXPENSES_FILE = 'data/expenses.db'
CATEGORIES_FILE = 'data/categories.db'

def load_categories():
    """Load categories from database or return default categories."""
    categories = fetch_all("SELECT category_name FROM categories")
    if not categories:
        return ['Food', 'Travel', 'Utilities', 'Entertainment', 'Miscellaneous']
    return [category[0] for category in categories]

def save_categories(categories):
    """Save categories in the database."""
    for category in categories:
        execute_query("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (category,))


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
                    execute_query("DELETE FROM categories WHERE category_name = ?", (removed,))
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

    # Insert the new expense into the database
    execute_query("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))

    print(f"Added Expense: {date} - {category} - ₹{amount}")

def display_expenses():
    expenses = fetch_all("SELECT * FROM expenses")
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    print("\nYour Expenses:")
    print(f"{'Date':<15}{'Category':<15}{'Amount':<10}")
    print("-" * 40)
    for row in expenses:
        print(f"{row[1]:<15}{row[2]:<15}₹{row[3]:<10}")

def delete_by_index():
    expenses = fetch_all("SELECT * FROM expenses")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("All Expenses")
    for i, row in enumerate(expenses, 1):
        print(f"{i}. {row[2]} - {row[1]} (Date: {row[1]})")
    
    try:
        index = int(input("\nEnter the index of the expense you want to delete: ")) - 1
        if index < 0 or index >= len(expenses):
            print("Invalid index. No expense found.")
            return
    except ValueError:
        print("Invalid index. Please enter a number.")
        return
    
    confirm = input(f"Are you sure you want to delete the expense: {expenses[index][2]} - {expenses[index][3]}?: ")
    if confirm.lower() == 'y':
        expense_id = expenses[index][0]
        execute_query("DELETE FROM expenses WHERE id = ?", (expense_id,))
        print("Expense deleted successfully.")
    else:
        print("Deletion cancelled.")

def delete_by_category():
    category_to_delete = input("Enter the category to delete(e.g., Food, Travel, etc): ").strip()
    
    expenses = fetch_all("SELECT * FROM expenses WHERE category = ?", (category_to_delete,))
    if not expenses:
        print(f"No expenses found for category '{category_to_delete}'")
        return

    execute_query("DELETE FROM expenses WHERE category = ?", (category_to_delete,))
    print(f"All expenses for category '{category_to_delete}' have been deleted.")

def delete_by_month_year():
    input_month, input_year = get_valid_month_year()
    if not is_valid_date(input_year, input_month):
        print("Invalid month/year input. Please try again.")
        return

    expenses = fetch_all("SELECT * FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (input_month, input_year))
    if not expenses:
        print("No expenses recorded for this month/year.")
        return

    execute_query("DELETE FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (input_month, input_year))
    print(f"All expenses for {input_month}/{input_year} have been deleted.")
