import json
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, db_connection, encryption_key):
        self.db_connection = db_connection
        self.fernet = Fernet(encryption_key)

    def add_saved_password(self, user_id, site_name, account_name, password):
        encrypted_site_name = self.encrypt(site_name)
        encrypted_account_name = self.encrypt(account_name)
        encrypted_password = self.encrypt(password)
        with self.db_connection:
            self.db_connection.execute(
                "INSERT INTO saved_passwords (user_id, encrypted_site_name, encrypted_account_name, encrypted_password) VALUES (?, ?, ?, ?)",
                (user_id, encrypted_site_name, encrypted_account_name, encrypted_password)
            )

    def get_saved_passwords_by_user_id(self, user_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT encrypted_site_name, encrypted_account_name, encrypted_password FROM saved_passwords WHERE user_id=?", (user_id,))
        encrypted_entries = cursor.fetchall()

        decrypted_entries = {}
        for encrypted_site_name, encrypted_account_name, encrypted_password in encrypted_entries:
            decrypted_site_name = self.decrypt(encrypted_site_name)
            decrypted_account_name = self.decrypt(encrypted_account_name)
            decrypted_password = self.decrypt(encrypted_password)
            
            if decrypted_site_name not in decrypted_entries:
                decrypted_entries[decrypted_site_name] = []
            
            decrypted_entries[decrypted_site_name].append({
                "account_name": decrypted_account_name,
                "password": decrypted_password
            })

            return json.dumps(decrypted_entries, indent=4)
      
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
        return self.fernet.encrypt(text_to_be_encrypted.encode()).decode()

    def decrypt(self, encrypted_text):
        return self.fernet.decrypt(encrypted_text.encode()).decode()