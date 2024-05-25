import logging
import json
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

class PasswordManager:
    def __init__(self, db_connection, encryption_key):
        self.db_connection = db_connection
        self.fernet = Fernet(encryption_key)
        logging.debug(f"Fernet initialized: {self.fernet}")

    def add_saved_password(self, user_id, site_name, account_name, password):
        try:
            encrypted_site_name = self.encrypt(site_name)
            encrypted_account_name = self.encrypt(account_name)
            encrypted_password = self.encrypt(password)
            with self.db_connection:
                self.db_connection.execute(
                    "INSERT INTO saved_passwords (user_id, encrypted_site_name, encrypted_account_name, encrypted_password) VALUES (?, ?, ?, ?)",
                    (user_id, encrypted_site_name, encrypted_account_name, encrypted_password)
                )
            return {"status": "success", "message": "Password successfully added"}
        except Exception as e:
            logging.error(f"Error adding password: {str(e)}")  # Log error
            return {"status": "error", "message": str(e)}

    def get_saved_passwords_by_user_id(self, user_id):
        logging.debug(f"user_id backend: {user_id}")  # Log to file
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT encrypted_site_name, encrypted_account_name, encrypted_password FROM saved_passwords WHERE user_id=?", (user_id,))
        encrypted_entries = cursor.fetchall()
        logging.debug(f"Encrypted Entries: {encrypted_entries}")  # Log to file

        decrypted_entries = {}
        for entry in encrypted_entries:
            if len(entry) != 3:
                logging.error(f"Entry has unexpected format: {entry}")
                continue
            encrypted_site_name, encrypted_account_name, encrypted_password = entry
            try:
                decrypted_site_name = self.decrypt(encrypted_site_name)
                decrypted_account_name = self.decrypt(encrypted_account_name)
                decrypted_password = self.decrypt(encrypted_password)

                if decrypted_site_name not in decrypted_entries:
                    decrypted_entries[decrypted_site_name] = []

                decrypted_entries[decrypted_site_name].append({
                    "account_name": decrypted_account_name,
                    "password": decrypted_password
                })
            except Exception as e:
                logging.error(f"Error decrypting entry: {str(e)}")  # Log decryption error

        sorted_decrypted_entries = {k: decrypted_entries[k] for k in sorted(decrypted_entries.keys())}
        
        logging.debug(f"Decrypted Entries: {sorted_decrypted_entries}")  # Log final decrypted entries
        return json.dumps(sorted_decrypted_entries, indent=4)

      
    def get_accountName_and_password_by_site_name(self, user_id, decrypted_site_name):
        cursor = self.db_connection.cursor()

        # Prepare SQL Query to retrieve all encrypted usernames and passwords for the user
        query = """
        SELECT encrypted_site_name, encrypted_account_name, encrypted_password FROM saved_passwords
        WHERE user_id = ?
        """
        cursor.execute(query, (user_id,))
        
        # Fetch all results
        results = cursor.fetchall()

        for encrypted_site_name, encrypted_account_name, encrypted_password in results:
            # Decrypt the site name
            decrypted_site = self.decrypt(encrypted_site_name)
            if decrypted_site == decrypted_site_name:
                # Decrypt the username and password if a match is found
                decrypted_accountName = self.decrypt(encrypted_account_name)
                decrypted_password = self.decrypt(encrypted_password)
                return {"accountName": decrypted_accountName, "password": decrypted_password}
        
        return None  # Or handle the case where no entry matches

    def edit_saved_password(self, password_id, site_name, account_name, password):
        encrypted_site_name = self.encrypt(site_name)
        encrypted_account_name = self.encrypt(account_name)
        encrypted_password = self.encrypt(password)

        with self.db_connection:
            self.db_connection.execute(
                "UPDATE saved_passwords SET encrypted_site_name = ?, encrypted_account_name = ?, encrypted_password = ? WHERE password_id = ?",
                (encrypted_site_name, encrypted_account_name, encrypted_password, password_id)
            )
            
    def delete_saved_password(self, password_id):
        with self.db_connection:
            self.db_connection.execute(
                "DELETE FROM saved_passwords WHERE password_id = ?",
                (password_id,)
            )
            
    def encrypt(self, text_to_be_encrypted):
        try:
            return self.fernet.encrypt(text_to_be_encrypted.encode()).decode()
        except Exception as e:
            logging.error(f"Error encrypting text: {str(e)}")
            raise e

    def decrypt(self, encrypted_text):
        try:
            return self.fernet.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            logging.error(f"Error decrypting text: {str(e)}")
            raise e