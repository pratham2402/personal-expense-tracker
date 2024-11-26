import csv
import os
import datetime

def read_csv(file_name):
    """Read CSV file and return content as list of dictionaries."""
    if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
        return []
    with open(file_name, 'r') as file:
        return list(csv.DictReader(file))

def write_csv(file_name, fieldnames, rows):
    """Write rows to a CSV file."""
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def get_valid_month_year():
    """Prompt user to input a valid month and year."""
    while True:
        try:
            month = int(input("Enter the month(MM): "))
            year = int(input("Enter the year(YYYY): "))
            if 1 <= month <= 12:
                return f"{month:02d}", str(year)
            else:
                print("Month must be between 1 and 12.")
        except ValueError:
            print("Enter valid numeric values for month and year.")

def file_exists(file_name):
    """Check if a file exists and is not empty."""
    return os.path.exists(file_name) and os.path.getsize(file_name) > 0

def is_valid_date(year, month):
    try:
        datetime.date(year = int(year), month = int(month), day=1)
        return True
    except ValueError:
        return False
