from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, db_connection, encryption_key):
        self.db_connection = db_connection
        self.fernet = Fernet(encryption_key)

    def add_password(self, user_id, site_name, account_name, password):
        encrypted_password = self.encrypt_password(password)
        with self.db_connection:
            self.db_connection.execute(
                "INSERT INTO saved_passwords (user_id, site_name, account_name, encrypted_password) VALUES (?, ?, ?, ?)",
                (user_id, site_name, account_name, encrypted_password)
            )

    def retrieve_passwords(self, user_id):
        # Retrieve all passwords for the given user_id
        # Decrypt the passwords before returning
        pass
      
    def encrypt_password(self, password):
        return self.fernet.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        return self.fernet.decrypt(encrypted_password.encode()).decode()