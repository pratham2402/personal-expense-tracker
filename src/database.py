import sqlite3

DATABASE_FILE = 'data/expenses.db'

def create_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT UNIQUE NOT NULL                   
                   )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT NOT NULL,
                   category TEXT NOT NULL,
                   amount REAL NOT NULL                   
                   )''')
    
    conn.commit()
    conn.close()

create_db()