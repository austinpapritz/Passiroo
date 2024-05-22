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
    if result:
        return json.dumps(result)
    else:
        return json.dumps({"status": "error", "message": "Login failed"})
  
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


def fetch_user_id():
    try:
        user_id = user_manager.current_user_id
        if user_id is None:
            return json.dumps({"status": "error", "message": "User not logged in"})
        return json.dumps({"status": "success", "user_id": user_id})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def fetch_passwords(user_id):
    try:
        passwords = password_manager.get_saved_passwords_by_user_id(user_id)
        if not passwords:
            passwords = []
        passwords_dict = {}
        for site, account_name, password in passwords:
            if site not in passwords_dict:
                passwords_dict[site] = []
            passwords_dict[site].append({
                'account_name': account_name,
                'password': password
            })
        return json.dumps(passwords_dict)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def logout_user():
    try:
        user_manager.logout_user()
        return json.dumps({"status": "success"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == '__main__':
    try:
        action = sys.argv[1]
        if action == 'register_user':
            email = sys.argv[2]
            password = sys.argv[3]
            print(register_user(email, password))
        elif action == 'login_user':
            email = sys.argv[2]
            password = sys.argv[3]
            print(login_user(email, password))
        elif action == 'logout_user':
            print(logout_user())
        elif action == 'fetch_user_id':
            print(fetch_user_id())
        elif action == 'fetch_passwords':
            user_id = sys.argv[2]
            print(fetch_passwords(user_id))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))