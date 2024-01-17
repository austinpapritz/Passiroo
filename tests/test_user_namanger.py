import unittest
import sqlite3
from py.user_manager import UserManager

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

    def test_userManager_hash_password_passwordDifferentThanHashed(self):
        # Assemble
        password = "example_password"
        hashed = self.user_manager.hash_password(password)
        # Assert
        self.assertNotEqual(password, hashed)

    def test_userManager_verify_password_hashedMatchesPassword(self):
        # Assemble
        password = "example_password"
        hashed = self.user_manager.hash_password(password)
        result = self.user_manager.verify_password(hashed, password)
        # Assert
        self.assertTrue(result)

    def test_userManager_register_user_checkDbForEmailAndPassword(self):
        # Assemble
        email = "test@example.com"
        password = "testpassword123"
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
        password = "testlogin123"
        # Act 
        self.user_manager.register_user(email, password)
        # Assert
        self.assertTrue(self.user_manager.login_user(email, password))

    def test_userManager_login_user_checkInvalidLoginByPassword(self):
        # Assemble
        email = "login_test@example.com"
        password = "testlogin123"
        # Act 
        self.user_manager.register_user(email, password)
        # Assert
        self.assertFalse(self.user_manager.login_user(email, "wrongpassword"))
        
    def test_userManager_login_user_checkInvalidLoginByEmail(self):
        # Assemble
        email = "login_test@example.com"
        password = "testlogin123"
        # Act 
        self.user_manager.register_user(email, password)
        # Assert
        self.assertFalse(self.user_manager.login_user("wrong@email.com", password))

    def tearDown(self):
      self.connection.close()

if __name__ == '__main__':
    unittest.main()