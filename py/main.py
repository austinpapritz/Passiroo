# Example main.py
import sqlite3
from py.Models.password_manager import PasswordManager

# Establish a database connection
db_connection = sqlite3.connect('Passiroo.db')

# Create an instance of PasswordManager
password_manager = PasswordManager(db_connection)

# Use password_manager to add, retrieve, update, or delete passwords
