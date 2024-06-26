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

logging.basicConfig(filename="python-app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_app_path():
    if getattr(sys, "frozen", False):  # If running as a compiled executable
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

app_path = get_app_path()
db_path = os.path.join(app_path, "passiroo.db")
key_path = os.path.join(app_path, "secret.key")

def save_key(key, filename="secret.key"):
    with open(filename, "wb") as key_file:
        key_file.write(key)
        
def generate_and_save_key(filename="secret.key"):
    key = Fernet.generate_key()
    save_key(key, filename)

def load_key(filename="secret.key"):
    return open(filename, "rb").read()

if not os.path.exists(db_path):
    create_database(db_path)

if not os.path.exists(key_path):
    generate_and_save_key(key_path)

db_connection = sqlite3.connect(db_path)
key = load_key(key_path)
password_manager = PasswordManager(db_connection, key)
page_manager = PageManager()
user_manager = UserManager(db_connection, app_path)

def register_and_login_user(email, password):
    result = user_manager.register_and_login_user(email, password)
    if result:
        return json.dumps(result)
    else:
        return json.dumps({"status": "error", "message": "Login failed"})

def login_user(email, password):
    result = user_manager.login_user(email, password)
    if result:
        return json.dumps(result)
    else:
        return json.dumps({"status": "error", "message": "Login failed"})
  
def add_site_account_and_password(user_id, site_name, account_name, password):
    try:
        password_manager.add_site_account_and_password_to_database(user_id, site_name, account_name, password)
        return json.dumps({"status": "success", "message": "Password successfully added"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
      
def edit_password(password_id, site_name, account_name, password):
    try:
        password_manager.edit_saved_password(password_id, site_name, account_name, password)
        return json.dumps({"status": "success", "message": "Password successfully edited"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
      
def delete_password(password_id):
    try:
        password_manager.delete_saved_password(password_id)
        return json.dumps({"status": "success", "message": "Password successfully deleted"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def generate_random_password(special_characters, password_length):
    try:
        password = page_manager.generate_random_password(special_characters, int(password_length))
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

def fetch_sites_accounts_and_passwords(user_id):
    try:
        passwords = password_manager.get_saved_sites_accounts_and_passwords_by_user_id(user_id)
        if not passwords:
            passwords = []
        return json.dumps({"status": "success", "data": passwords})
    except Exception as e:
        logging.error(f"Error fetching passwords: {str(e)}") 
        return json.dumps({"status": "error", "message": str(e)})

def logout_user():
    try:
        user_manager.logout_user()
        return json.dumps({"status": "success"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    try:
        action = sys.argv[1]
        if action == "register_and_login_user":
            email = sys.argv[2]
            password = sys.argv[3]
            print(register_and_login_user(email, password))
        elif action == "login_user":
            email = sys.argv[2]
            password = sys.argv[3]
            print(login_user(email, password))
        elif action == "logout_user":
            print(logout_user())
        elif action == "add_site_account_and_password":
            user_id = sys.argv[2]
            site_name = sys.argv[3]
            account_name = sys.argv[4]
            password = sys.argv[5]
            print(add_site_account_and_password(user_id, site_name, account_name, password))
        elif action == "generate_random_password":
            special_characters = sys.argv[2]
            password_length = sys.argv[3]
            print(generate_random_password(special_characters, password_length))
        elif action == "edit_password":
            password_id = sys.argv[2]
            site_name = sys.argv[3]
            account_name = sys.argv[4]
            password = sys.argv[5]
            print(edit_password(password_id, site_name, account_name, password ))
        elif action == "delete_password":
            password_id = sys.argv[2]
            print(delete_password(password_id))
        elif action == "fetch_user_id":
            print(fetch_user_id())
        elif action == "fetch_sites_accounts_and_passwords":
            user_id = sys.argv[2]
            print(fetch_sites_accounts_and_passwords(user_id))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))