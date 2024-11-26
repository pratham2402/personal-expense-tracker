import sqlite3
import datetime

DATABASE = 'data/expenses.db'

def connect_db():
    """Connect to SQLite database and return the connection object."""
    conn = sqlite3.connect(DATABASE)
    return conn

def execute_query(query, params=()):
    """Execute a query that doesn't return data (like INSERT, DELETE, UPDATE)."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(query, params=()):
    """Execute a SELECT query and return all results."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

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


def is_valid_date(year, month):
    """Check if the year and month form a valid date."""
    try:
        datetime.date(year = int(year), month = int(month), day=1)
        return True
    except ValueError:
        return False
