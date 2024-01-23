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
                password_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
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
    
    def test_passwordManager_retrieve_saved_passwords_savedDataMatchesFetchedData(self):
        # Assemble
        user_id = 1 
        site_name = "example1.com"
        account_name = "user1@example.com"
        password = "password123"
        
        user_id = 1 
        site_name2 = "example2.com"
        account_name2 = "user2@example.com"
        password2 = "password2123"

        # Act
        self.password_manager.add_saved_password(user_id, site_name, account_name, password)
        self.password_manager.add_saved_password(user_id, site_name2, account_name2, password2)
        retrieved_entries = self.password_manager.retrieve_saved_passwords(user_id)

        # Assert
        self.assertEqual(len(retrieved_entries), 2)

        decrypted_site_name, decrypted_account_name, decrypted_password = retrieved_entries[0]
        self.assertEqual(decrypted_site_name, site_name)
        self.assertEqual(decrypted_account_name, account_name)
        self.assertEqual(decrypted_password, password)
        
        decrypted_site_name2, decrypted_account_name2, decrypted_password2 = retrieved_entries[1]
        self.assertEqual(decrypted_site_name2, site_name2)
        self.assertEqual(decrypted_account_name2, account_name2)
        self.assertEqual(decrypted_password2, password2)

    def test_password_manager_edit_saved_password_newDataMatchesFetchedData(self):
        # Assemble
        user_id = 1
        original_site_name = "example.com"
        original_account_name = "user@example.com"
        original_password = "password123"
        new_site_name = "newexample.com"
        new_account_name = "newuser@example.com"
        new_password = "newpassword456"

        # Act
        self.password_manager.add_saved_password(user_id, original_site_name, original_account_name, original_password)
        cursor = self.connection.cursor()
        cursor.execute("SELECT password_id FROM saved_passwords WHERE user_id=?", (user_id,))
        password_entry = cursor.fetchone()
        self.assertIsNotNone(password_entry)
        password_id = password_entry[0]

        # Edit the password, site name, and account name
        self.password_manager.edit_saved_password(password_id, new_site_name, new_account_name, new_password)

        # Assert
        retrieved_entries = self.password_manager.retrieve_saved_passwords(user_id)
        self.assertEqual(len(retrieved_entries), 1)
        decrypted_site_name, decrypted_account_name, decrypted_password = retrieved_entries[0]
        self.assertEqual(decrypted_site_name, new_site_name)
        self.assertEqual(decrypted_account_name, new_account_name)
        self.assertEqual(decrypted_password, new_password)

if __name__ == '__main__':
    unittest.main()
