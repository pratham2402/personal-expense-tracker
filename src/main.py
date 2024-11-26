from utils import *
from data_analysis import *
from expense_management import *


# Ensure the database is ready
conn = connect_db()
conn.close()

print("Welcome to Your Personal Expense Tracker")
while True:
    try:
        print("\nMenu Options:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Category Summary")
        print("4. Display Monthly Report")
        print("5. Delete Expenses")
        print("6. Sort Expenses")
        print("7. Export Data")
        print("8. Visualize Expenses")
        print("9. Filter Expenses")
        print("10. Create Backup")
        print("11. Monthly Expenses Visualized")
        print("12. Manage Categories")
        print("13. Exit")
        
        user_ans = int(input("Choose an option (1-13): "))
        
    except ValueError:
        print('Enter a valid number.')
        continue

    if user_ans == 1:
        add_expense()
    elif user_ans == 2:
        display_expenses()
    elif user_ans == 3:
        category_summary()
    elif user_ans == 4:
        display_monthly_report()
    elif user_ans == 5:
        # Sub-menu created for deleting records
        while True:
            try:
                print("\nDeletion Options:")
                print("1. Delete record by index")
                print("2. Delete by category")
                print("3. Delete by month & year")
                user_delete_choice = int(input("Choose an option (1-3): "))
            except ValueError:
                print("Enter a valid number")
                continue
            if user_delete_choice == 1: 
                delete_by_index()
                break
            elif user_delete_choice == 2:
                delete_by_category()
                break
            elif user_delete_choice == 3:
                delete_by_month_year()
                break
    elif user_ans == 6:
        sort_expenses()
    elif user_ans == 7:
        export_data()
    elif user_ans == 8:
        visualize_expenses()
    elif user_ans == 9:
        filter_expenses()
    elif user_ans == 10:
        create_backup()
    elif user_ans == 11:
        monthly_expense_trends()
    elif user_ans == 12:
        manage_category()
    elif user_ans == 13:
        print('Goodbye!')
        break
    else:
        print("Invalid option. Try again.")
