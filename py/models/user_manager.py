import bcrypt

class UserManager(object):
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self._current_user_id = None
        
    @property
    def current_user_id(self):
        return self._current_user_id

    @current_user_id.setter
    def current_user_id(self, value):
        self._current_user_id = value

    @current_user_id.deleter
    def current_user_id(self):
        del self._current_user_id

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
        self.login_user(email, password)

    def login_user(self, email, provided_password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        print('result of email match', result)
        if result is None:
            return False  # False if User not found

        stored_hashed_password = result[0]
        pw_check_bool = bcrypt.checkpw(provided_password.encode(), stored_hashed_password)
        print('pw check', pw_check_bool)
        if pw_check_bool is True:
            user_id = self.get_user_id_by_email(email)
            if user_id:
              print('user_id', user)
              UserManager.current_user_id = user_id
              return True
            else: 
              return False
        else:
            return False

    def logout_user(self):
        del UserManager.current_user_id

    def get_user_id_by_email(self, email):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        
        if result is None:
            return None

        return result[0]  # user_id