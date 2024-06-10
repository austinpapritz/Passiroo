import json
import sqlite3
import unittest
from cryptography.fernet import Fernet
from py.models.password_manager import PasswordManager

# Navigate to project folder and run tests with 
#   `python -m unittest discover -s tests`

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.db_connection = sqlite3.connect(":memory:")
        self.db_connection.execute("""
            CREATE TABLE saved_passwords (
                password_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                encrypted_site_name TEXT NOT NULL,
                encrypted_account_name TEXT NOT NULL,
                encrypted_password TEXT NOT NULL
            );
        """)
        key = load_key()
        self.password_manager = PasswordManager(self.db_connection, key)

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
        cursor = self.db_connection.cursor()
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
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT password_id FROM saved_passwords WHERE user_id=?", (user_id,))
        password_entry = cursor.fetchone()
        self.assertIsNotNone(password_entry)
        password_id = password_entry[0]

        # Edit the password, site name, and account name
        self.password_manager.edit_saved_password(password_id, new_site_name, new_account_name, new_password)

        # Assert
        retrieved_entries_json = self.password_manager.get_saved_passwords_by_user_id(user_id)
        retrieved_entries = json.loads(retrieved_entries_json)

        # Check that we have exactly one site entry for the new site name
        self.assertIn(new_site_name, retrieved_entries)
        site_entries = retrieved_entries[new_site_name]
        self.assertEqual(len(site_entries), 1)

        decrypted_entry = site_entries[0]
        decrypted_account_name = decrypted_entry["account_name"]
        decrypted_password = decrypted_entry["password"]

        self.assertEqual(decrypted_account_name, new_account_name)
        self.assertEqual(decrypted_password, new_password)

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
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT password_id FROM saved_passwords WHERE user_id=?", (user_id,))
        password_entry = cursor.fetchone()
        self.assertIsNotNone(password_entry)
        password_id = password_entry[0]

        # Edit the password, site name, and account name
        self.password_manager.edit_saved_password(password_id, new_site_name, new_account_name, new_password)

        # Assert
        retrieved_entries_json = self.password_manager.get_saved_passwords_by_user_id(user_id)
        retrieved_entries = json.loads(retrieved_entries_json)

        # Check that we have exactly one site entry for the new site name
        self.assertIn(new_site_name, retrieved_entries)
        site_entries = retrieved_entries[new_site_name]
        self.assertEqual(len(site_entries), 1)

        site_name = site_entries[0]
        retrieved_account_name = site_name["account_name"]
        retrieved_password = site_name["password"]

        self.assertEqual(retrieved_account_name, new_account_name)
        self.assertEqual(retrieved_password, new_password)


        
    def test_password_manager_get_accountName_and_password_by_site_name_fetchedDataMatchesSavedData(self):
        # Assemble
        user_id = 1
        site_name = "www.retrievebysite.com"
        account_name = "user@example.com"
        password = "password123"

        # Act
        self.password_manager.add_saved_password(user_id, site_name, account_name, password)
        results = self.password_manager.get_accountName_and_password_by_site_name(user_id, site_name)
        
        # Assert
        self.assertEqual(results["accountName"], account_name)
        self.assertEqual(results["password"], password)
    
def load_key(filename="secret.key"):
    with open(filename, "rb") as key_file:
        return key_file.read()

if __name__ == "__main__":
    unittest.main()
