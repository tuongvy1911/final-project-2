import tkinter as tk
from tkinter import messagebox, scrolledtext
from database import Database

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Perform authentication (dummy authentication for demonstration)
        if username == "admin" and password == "password":
            self.master.destroy()
            root = tk.Tk()
            app = BankApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class BankApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MyBank - Your Personal Banking Solution")

        # Connect to SQLite database
        self.db = Database()

        # Load account balance from file
        self.load_balance()

        # Create the main window layout
        self.create_layout()

    def create_layout(self):
        # Welcome message
        self.welcome_label = tk.Label(self.master, text="Welcome to MyBank!", font=("Helvetica", 16, "bold"))
        self.welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create account balance label
        self.balance_label = tk.Label(self.master, text=f"Account Balance: ${self.balance}", font=("Helvetica", 12))
        self.balance_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Create entry widget for amount
        self.amount_entry = tk.Entry(self.master, font=("Helvetica", 12), width=15)
        self.amount_entry.grid(row=2, column=0, columnspan=2, pady=5)

        # Create buttons for different transaction categories
        self.create_buttons()

    def create_buttons(self):
        # Create a frame to contain the buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=5)

        # Create buttons for different transaction categories
        categories = ["Deposit", "Withdraw", "Bill Payment", "Transaction History", "Quit"]
        button_width = 20
        button_height = 2

        for i, category in enumerate(categories):
            button = tk.Button(self.button_frame, text=category, command=lambda cat=category: self.handle_transaction(cat), width=button_width, height=button_height)
            button.grid(row=i // 2, column=i % 2, padx=5, pady=5)

    def handle_transaction(self, category):
        if category == "Deposit":
            self.deposit()
        elif category == "Withdraw":
            self.withdraw()
        elif category == "Bill Payment":
            self.pay_bill()
        elif category == "Transaction History":
            self.show_history()
        elif category == "Quit":
            self.save_balance()  # Save balance before quitting
            self.quit()

    def load_balance(self):
        try:
            with open("balance.txt", "r") as file:
                self.balance = float(file.read())
        except FileNotFoundError:
            self.balance = 0

    def save_balance(self):
        with open("balance.txt", "w") as file:
            file.write(str(self.balance))

    def update_balance_label(self):
        self.balance_label.config(text=f"Account Balance: ${self.balance}")

    def clear_entry(self):
        self.amount_entry.delete(0, tk.END)

    def get_amount(self):
        try:
            amount = float(self.amount_entry.get())
            self.clear_entry()  # Clear entry after getting amount
            return amount
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return None

    def deposit(self):
        amount = self.get_amount()
        if amount is not None and amount > 0:
            self.balance += amount
            self.update_balance_label()
            self.db.save_transaction("Deposit", amount)
            messagebox.showinfo("Deposit", f"Deposited ${amount} successfully.")

    def withdraw(self):
        amount = self.get_amount()
        if amount is not None and 0 < amount <= self.balance:
            self.balance -= amount
            self.update_balance_label()
            self.db.save_transaction("Withdraw", amount)
            messagebox.showinfo("Withdrawal", f"Withdrew ${amount} successfully.")
        elif amount is not None:
            messagebox.showerror("Error", "Insufficient funds or invalid amount for withdrawal.")

    def pay_bill(self):
        amount = self.get_amount()
        if amount is not None and 0 < amount <= self.balance:
            self.balance -= amount
            self.update_balance_label()
            self.db.save_transaction("Bill Payment", amount)
            messagebox.showinfo("Bill Payment", f"Paid bill of ${amount} successfully.")
        elif amount is not None:
            messagebox.showerror("Error", "Insufficient funds or invalid bill amount.")

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Transaction History")

        history_text = scrolledtext.ScrolledText(history_window, width=40, height=10, wrap=tk.WORD)
        history_text.pack()

        transactions = self.db.get_transactions()
        for transaction in transactions:
            history_text.insert(tk.END, f"{transaction[1]} - ${transaction[2]} - {transaction[3]}\n")

        history_text.config(state=tk.DISABLED)

    def quit(self):
        self.db.close_connection()
        self.master.destroy()

def main():
    login_root = tk.Tk()
    login_window = LoginWindow(login_root)
    login_root.mainloop()

if __name__ == "__main__":
    main()