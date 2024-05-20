import sqlite3
import sys
import json
from cryptography.fernet import Fernet
from models.password_manager import PasswordManager
from models.user_manager import UserManager

from initialize_db import create_database

# Establish a database connection
db_connection = sqlite3.connect('passiroo.db')

# Create an instance of PasswordManager
# key = Fernet.generate_key()
# password_manager = PasswordManager(db_connection, key)

# Create an instance of UserManager
user_manager = UserManager(db_connection)

create_database()

def register_user(email, password):
    result = user_manager.register_user(email, password)
    return json.dumps(result)

def login_user(email, password):
    result = user_manager.login_user(email, password)
    return json.dumps(result)

if __name__ == '__main__':
    action = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    if action == 'register_user':
        print(register_user(email, password))
    elif action == 'login_user':
        print(login_user(email, password))