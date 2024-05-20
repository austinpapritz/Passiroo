import sqlite3
import sys
import json
from cryptography.fernet import Fernet
from models.page_manager import PageManager
from models.password_manager import PasswordManager
from models.user_manager import UserManager

from initialize_db import create_database

# Establish a database connection
db_connection = sqlite3.connect('passiroo.db')

# Create an instance of PasswordManager
key = Fernet.generate_key()
password_manager = PasswordManager(db_connection, key)

# Create an instance of PageManager
page_manager = PageManager()

# Create an instance of UserManager
user_manager = UserManager(db_connection)

create_database()

def register_user(email, password):
    result = user_manager.register_user(email, password)
    return json.dumps(result)

def login_user(email, password):
    result = user_manager.login_user(email, password)
    return json.dumps(result)
  
def add_password(website, email, password):
    try:
        password_manager.add_saved_password(website, email, password)
        return json.dumps({"status": "success"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def generate_random_password(spec_chars, pw_length):
    try:
        password = page_manager.create_random_password(spec_chars, int(pw_length))
        return json.dumps({"status": "success", "password": password})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})  

if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'register_user':
        email = sys.argv[2]
        password = sys.argv[3]
        print(register_user(email, password))
    elif action == 'login_user':
        email = sys.argv[2]
        password = sys.argv[3]
        print(login_user(email, password))
    elif action == 'add_password':
        website = sys.argv[2]
        email = sys.argv[3]
        password = sys.argv[4]
        print(add_password(website, email, password))
    elif action == 'generate_random_password':
        spec_chars = sys.argv[2]
        pw_length = sys.argv[3]
        print(generate_random_password(spec_chars, pw_length))