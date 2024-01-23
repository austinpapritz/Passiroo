import bcrypt

class UserManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def verify_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode(), stored_password)

    def register_user(self, email, password):
        hashed_password = self.hash_password(password)
        with self.db_connection:
            self.db_connection.execute(
                "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
                (email, hashed_password)
            )

    def login_user(self, email, provided_password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        if result is None:
            return False  # False if User not found

        stored_hashed_password = result[0]
        return bcrypt.checkpw(provided_password.encode(), stored_hashed_password) # Return bool if pw matches or not

    def get_user_id(self, email):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        
        if result is None:
            return None

        return result[0]  # user_id