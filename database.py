import sqlite3

class Database:
    def __init__(self, db_name="bank.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           category TEXT, 
                           amount REAL, 
                           date TEXT)''')
        self.conn.commit()

    def save_transaction(self, category, amount):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO transactions (category, amount, date) VALUES (?, ?, CURRENT_TIMESTAMP)", (category, amount))
        self.conn.commit()

    def get_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()
