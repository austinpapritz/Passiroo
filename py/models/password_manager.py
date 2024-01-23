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
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT encrypted_site_name, encrypted_account_name, encrypted_password FROM saved_passwords WHERE user_id=?", (user_id,))
        encrypted_entries = cursor.fetchall()

        decrypted_entries = []
        for encrypted_site_name, encrypted_account_name, encrypted_password in encrypted_entries:
            decrypted_site_name = self.decrypt(encrypted_site_name)
            decrypted_account_name = self.decrypt(encrypted_account_name)
            decrypted_password = self.decrypt(encrypted_password)
            decrypted_entries.append((decrypted_site_name, decrypted_account_name, decrypted_password))

        return decrypted_entries

    def edit_saved_password(self, password_id, site_name, account_name, password):
        encrypted_site_name = self.encrypt(site_name)
        encrypted_account_name = self.encrypt(account_name)
        encrypted_password = self.encrypt(password)

        with self.db_connection:
            self.db_connection.execute(
                "UPDATE saved_passwords SET encrypted_site_name = ?, encrypted_account_name = ?, encrypted_password = ? WHERE password_id = ?",
                (encrypted_site_name, encrypted_account_name, encrypted_password, password_id)
            )

    def encrypt(self, text_to_be_encrypted):
        return self.fernet.encrypt(text_to_be_encrypted.encode()).decode()

    def decrypt(self, encrypted_text):
        return self.fernet.decrypt(encrypted_text.encode()).decode()