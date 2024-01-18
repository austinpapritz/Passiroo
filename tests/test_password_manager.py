import unittest
import sqlite3
from py.models.password_manager import PasswordManager

# Navigate to project folder and run tests with 
#   `python -m unittest discover -s tests`

class TestPasswordManager(unittest.TestCase):
  # unittest runs setUp() before each test
    def setUp(self):
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute("""
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            );
        """)
        self.password_manager = PasswordManager(self.connection)

    def test_passwordManager_encrypt_password_passwordDifferentThanEncryption(self):
        # Assemble
        password = "example_password"
        # Act
        encryptedPassword = self.password_manager.encrypt_password(password)
        # Assert
        self.assertNotEqual(password, encryptedPassword)

if __name__ == '__main__':
    unittest.main()
