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
                encrypted_site_name TEXT NOT NULL,
                encrypted_account_name TEXT NOT NULL,
                encrypted_password TEXT NOT NULL
            );
        """)
        key = Fernet.generate_key()
        self.password_manager = PasswordManager(self.connection, key)

    def test_passwordManager_encrypt_passwordDifferentThanEncryption(self):
        # Assemble
        password = "example_password"
        # Act
        encryptedPassword = self.password_manager.encrypt(password)
        # Assert
        self.assertNotEqual(password, encryptedPassword)

    def test_passwordManager_decrypt_passwordEqualsDecryptedPassword(self):
        # Assemble
        password = "example_password"
        encryptedPassword = self.password_manager.encrypt(password)
        # Act
        decryptedPassword = self.password_manager.decrypt(encryptedPassword)
        # Assert
        self.assertEqual(password, decryptedPassword)

    def test_passwordManager_add_saved_password_passwordDataMatchesFetchedData(self):
        # Assemble
        user_id = 1
        site_name = "example.com"
        account_name = "user@example.com"
        password = "password123"
        # Act
        self.password_manager.add_saved_password(user_id, site_name, account_name, password)
        # Assert
        cursor = self.connection.cursor()
        cursor.execute("SELECT encrypted_site_name, encrypted_account_name, encrypted_password FROM saved_passwords WHERE user_id=?", 
                      (user_id,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        fetched_encrypted_site_name, fetched_encrypted_account_name, fetched_encrypted_password = result
        decrypted_fetched_site_name = self.password_manager.decrypt(fetched_encrypted_site_name)
        decrypted_fetched_account_name = self.password_manager.decrypt(fetched_encrypted_account_name)
        decrypted_fetched_password = self.password_manager.decrypt(fetched_encrypted_password)

        self.assertEqual(decrypted_fetched_site_name, site_name)
        self.assertEqual(decrypted_fetched_account_name, account_name)
        self.assertEqual(decrypted_fetched_password, password)

if __name__ == '__main__':
    unittest.main()
