import unittest
import sqlite3
from py.models.user_manager import UserManager

# Navigate to project folder and run tests with 
#   `python -m unittest discover -s tests`

class TestUserManager(unittest.TestCase):
  # unittest runs setUp() before each test
    def setUp(self):
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute("""
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            );
        """)
        self.user_manager = UserManager(self.connection)

    def test_password_validator_short_password(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.password_validator("Short1!")
        self.assertEqual(str(context.exception), "Password must be at least 11 characters long.")

    def test_password_validator_no_uppercase(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.password_validator("lowercase1!")
        self.assertEqual(str(context.exception), "Password must contain at least one uppercase letter.")

    def test_password_validator_no_lowercase(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.password_validator("UPPERCASE1!!!")
        self.assertEqual(str(context.exception), "Password must contain at least one lowercase letter.")

    def test_password_validator_no_number(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.password_validator("NoNumberrrrr!")
        self.assertEqual(str(context.exception), "Password must contain at least one number.")

    def test_password_validator_no_special_character(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.password_validator("NoSpecial123")
        self.assertEqual(str(context.exception), "Password must contain at least one special character (!@#&%^&._-).")

    def test_password_validator_valid_password(self):
        # This should not raise any exceptions
        try:
            self.user_manager.password_validator("ValidPass1!")
        except ValueError:
            self.fail("password_validator() raised ValueError unexpectedly!")
            
    def test_userManager_login_user_setsCurrentUserId(self):
        # Assemble
        account_name = "sotesty@gmail.com"
        password = "example_passworD123"
        self.user_manager.register_user(account_name, password) # runs login_user() after registering

        # Act
        user_id = self.user_manager.get_user_id_by_email(account_name)
        results = self.user_manager.current_user_id

        # Assert
        self.assertEqual(user_id, results)

    def test_userManager_UserManager_delCurrentUserId(self):
        # Assemble
        account_name = "sotesty@gmail.com"
        password = "example_passworD123"
        self.user_manager.register_user(account_name, password) # runs login_user() after registering

        # Act
        results = self.user_manager.current_user_id
        self.assertIsNotNone(results)
        del UserManager.current_user_id

        # Assert
        with self.assertRaises(AttributeError):
          _ = self.user_manager.current_user_id

    def test_userManager_hash_password_passwordDifferentThanHashed(self):
        # Assemble
        password = "example_password#123"
        # Act
        hashed = self.user_manager.hash_password(password)
        # Assert
        self.assertNotEqual(password, hashed)

    def test_userManager_verify_password_hashedMatchesPassword(self):
        # Assemble
        password = "example_passworD#123"
        #Act
        hashed = self.user_manager.hash_password(password)
        result = self.user_manager.verify_password(hashed, password)
        # Assert
        self.assertTrue(result)

    def test_userManager_register_user_checkDbForEmailAndPassword(self):
        # Assemble
        email = "test@example.com"
        password = "testpassworD#123"
        self.user_manager.register_user(email, password)
        # Act
        cursor = self.connection.cursor()
        cursor.execute("SELECT email, hashed_password FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        # Assert
        self.assertIsNotNone(user)
        self.assertEqual(user[0], email)
        self.assertNotEqual(user[1], password)
    
    def test_userManager_login_user_checkValidLogin(self):
        # Assemble
        email = "login_test@example.com"
        password = "testlogiN#123"
        # Act 
        self.user_manager.register_user(email, password)
        # Assert
        self.assertTrue(self.user_manager.login_user(email, password))

    def test_userManager_login_user_checkInvalidLoginByPassword(self):
        # Assemble
        email = "login_test@example.com"
        password = "testlogiN#123"
        # Act 
        self.user_manager.register_user(email, password)
        # Assert
        self.assertFalse(self.user_manager.login_user(email, "wrongpassword"))
        
    def test_userManager_login_user_checkInvalidLoginByEmail(self):
        # Assemble
        email = "login_test@example.com"
        password = "testlogiN#123"
        # Act 
        self.user_manager.register_user(email, password)
        # Assert
        self.assertFalse(self.user_manager.login_user("wrong@email.com", password))
        
    def test_userManager_get_user_id_by_email_checkUserIdIsInt(self):
        # Assemble
        email = "test@example.com"
        password = "passworD#123"

        # Act
        self.user_manager.register_user(email, password)
        
        # Retrieve the user ID
        user_id = self.user_manager.get_user_id_by_email(email)
        self.assertIsNotNone(user_id)
        self.assertIsInstance(user_id, int)

    def tearDown(self):
      self.connection.close()

if __name__ == '__main__':
    unittest.main()
