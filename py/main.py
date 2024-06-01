import logging
import sqlite3
import sys
import json
import os
from cryptography.fernet import Fernet
from models.page_manager import PageManager
from models.password_manager import PasswordManager
from models.user_manager import UserManager

from initialize_db import create_database

def save_key(key, filename="secret.key"):
    with open(filename, "wb") as key_file:
        key_file.write(key)
        
def generate_and_save_key(filename="secret.key"):
    key = Fernet.generate_key()
    save_key(key, filename)

def load_key(filename="secret.key"):
    return open(filename, "rb").read()

# Establish a database connection
db_connection = sqlite3.connect('passiroo.db')

# Create an instance of PasswordManager
key = load_key()
password_manager = PasswordManager(db_connection, key)

# Create an instance of PageManager
page_manager = PageManager()

# Create an instance of UserManager
user_manager = UserManager(db_connection)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

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
  
def add_password(user_id, site_name, account_name, password):
    try:
        logging.debug(f"Password added for site_name: {site_name}, account_name: {account_name}, user_id: {user_id}, password: {password}")
        password_manager.add_saved_password(user_id, site_name, account_name, password)
        return json.dumps({"status": "success", "message": "Password successfully added"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
      
def edit_password(password_id, site_name, account_name, password):
    try:
        logging.debug(f"Password (id {password_id}), added for site_name: {site_name}, account_name: {account_name}, password: {password}")
        password_manager.edit_saved_password(password_id, site_name, account_name, password)
        return json.dumps({"status": "success", "message": "Password successfully edited"})
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
        # logging.debug(f"Fetched Passwordss: {passwords}")  # Log to file
        if not passwords:
            passwords = []
        return json.dumps({"status": "success", "data": passwords})
    except Exception as e:
        logging.error(f"Error fetching passwords: {str(e)}")  # Log to file
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
        elif action == 'add_password':
            user_id = sys.argv[2]
            site_name = sys.argv[3]
            account_name = sys.argv[4]
            password = sys.argv[5]
            print(add_password(user_id, site_name, account_name, password))
        elif action == 'edit_password':
            password_id = sys.argv[2]
            site_name = sys.argv[3]
            account_name = sys.argv[4]
            password = sys.argv[5]
            print(edit_password(password_id, site_name, account_name, password))
        elif action == 'fetch_user_id':
            print(fetch_user_id())
        elif action == 'fetch_passwords':
            user_id = sys.argv[2]
            print(fetch_passwords(user_id))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))