import json
import pandas as pd
from datetime import datetime

# Class for User
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def register(username, password):
        # Load user data
        with open('users.json', 'r+') as file:
            users = json.load(file)
            if username in users:
                print("User already exists.")
                return False
            users[username] = {'password': password}
            file.seek(0)
            json.dump(users, file, indent=4)
        return True

    @staticmethod
    def login(username, password):
        with open('users.json', 'r') as file:
            users = json.load(file)
            if username in users and users[username]['password'] == password:
                print("Login successful.")
                return True
            print("Invalid username or password.")
            return False

# Class for FinanceRecord
class FinanceRecord:
    def __init__(self, description, amount, category, date):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = datetime.strptime(date, '%Y-%m-%d')

    def to_dict(self):
        return {
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.strftime('%Y-%m-%d')
        }

# Class for FinanceManager
class FinanceManager:
    def __init__(self, username):
        self.username = username
        self.finances_file = 'finances.json'
        self.finances = self.load_finances()

    def load_finances(self):
        try:
            with open(self.finances_file, 'r') as file:
                data = json.load(file)
                return data.get(self.username, [])
        except FileNotFoundError:
            return []

    def save_finances(self):
        try:
            with open(self.finances_file, 'r+') as file:
                data = json.load(file)
                data[self.username] = self.finances
                file.seek(0)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(self.finances_file, 'w') as file:
                json.dump({self.username: self.finances}, file, indent=4)

    def add_record(self, record):
        self.finances.append(record.to_dict())
        self.save_finances()

    def delete_record(self, index):
        if 0 <= index < len(self.finances):
            del self.finances[index]
            self.save_finances()
        else:
            print("Invalid record index.")

    def update_record(self, index, new_record):
        if 0 <= index < len(self.finances):
            self.finances[index] = new_record.to_dict()
            self.save_finances()
        else:
            print("Invalid record index.")

    def generate_report(self):
        df = pd.DataFrame(self.finances)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            print("\nTotal Income and Expenses:")
            print(df.groupby('category')['amount'].sum())
            
            print("\nSpending distribution by category:")
            print(df.groupby('category')['amount'].sum() / df['amount'].sum() * 100)
            
            print("\nMonthly trends:")
            print(df.groupby(df['date'].dt.to_period("M"))['amount'].sum())
        else:
            print("No records available for this user.")

# Example usage
if __name__ == "__main__":
    # User registration and login
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if User.register(username, password):
        print("Registration successful. Please log in.")
    
    if User.login(username, password):
        manager = FinanceManager(username)
        while True:
            print("\n1. Add record\n2. Delete record\n3. Update record\n4. Generate report\n5. Exit")
            choice = int(input("Choose an option: "))
            
            if choice == 1:
                desc = input("Enter description: ")
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                date = input("Enter date (YYYY-MM-DD): ")
                record = FinanceRecord(desc, amount, category, date)
                manager.add_record(record)
            elif choice == 2:
                index = int(input("Enter record index to delete: "))
                manager.delete_record(index)
            elif choice == 3:
                index = int(input("Enter record index to update: "))
                desc = input("Enter new description: ")
                amount = float(input("Enter new amount: "))
                category = input("Enter new category: ")
                date = input("Enter new date (YYYY-MM-DD): ")
                new_record = FinanceRecord(desc, amount, category, date)
                manager.update_record(index, new_record)
            elif choice == 4:
                manager.generate_report()
            elif choice == 5:
                break
