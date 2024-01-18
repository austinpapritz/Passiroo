from cryptography.fernet import Fernet
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
            CREATE TABLE saved_passwords (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL,
                account_name TEXT NOT NULL,
                encrypted_password TEXT NOT NULL
            );
        """)
        key = Fernet.generate_key()
        self.password_manager = PasswordManager(self.connection, key)

    def test_passwordManager_encrypt_password_passwordDifferentThanEncryption(self):
        # Assemble
        password = "example_password"
        # Act
        encryptedPassword = self.password_manager.encrypt_password(password)
        # Assert
        self.assertNotEqual(password, encryptedPassword)

    def test_passwordManager_decrypt_password_passwordEqualsDecryptedPassword(self):
        # Assemble
        password = "example_password"
        encryptedPassword = self.password_manager.encrypt_password(password)
        # Act
        decryptedPassword = self.password_manager.decrypt_password(encryptedPassword)
        # Assert
        self.assertEqual(password, decryptedPassword)

    def test_passwordManager_add_password_passwordDataMatchesFetchedData(self):
        # Assemble
        user_id = 1
        site_name = "example.com"
        account_name = "user@example.com"
        password = "password123"
        # Act
        self.password_manager.add_password(user_id, site_name, account_name, password)
        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT encrypted_password FROM saved_passwords WHERE user_id=? AND site_name=? AND account_name=?", 
                      (user_id, site_name, account_name))
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        encrypted_password = result[0]
        self.assertNotEqual(password, encrypted_password)
        decrypted_password = self.password_manager.decrypt_password(encrypted_password)
        self.assertEqual(password, decrypted_password)


if __name__ == '__main__':
    unittest.main()
