# Example main.py
import sqlite3
import sys
import json
from py.models.password_manager import PasswordManager
from py.models.user_manager import UserManager

# Establish a database connection
db_connection = sqlite3.connect('passiroo.db')

# Create an instance of PasswordManager
password_manager = PasswordManager(db_connection)

# Create an instance of UserManager
user_manager = UserManager(db_connection)

def register_user(email, password):
    print('registering user')
    try:
        user_manager.register_user(email, password)
        return json.dumps({"status": "success"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# Assuming the script is called with arguments
if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'register_user':
        email = sys.argv[2]
        password = sys.argv[3]
        print(register_user(email, password))