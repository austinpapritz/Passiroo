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

    def retrieve_saved_passwords(self, user_id):
        # Retrieve all passwords for the given user_id
        # Decrypt the passwords before returning
        pass
      
    def encrypt(self, text_to_be_encrypted):
        return self.fernet.encrypt(text_to_be_encrypted.encode()).decode()

    def decrypt(self, encrypted_text):
        return self.fernet.decrypt(encrypted_text.encode()).decode()