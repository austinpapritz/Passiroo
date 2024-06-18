import json
import os
import sqlite3
import unittest
from app.backend.models.user_manager import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.db_connection = sqlite3.connect(':memory:')
        self.db_connection.execute("""
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            );
        """)

        self.user_manager = UserManager(self.db_connection)

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
        self.user_manager.register_and_login_user(account_name, password)

        # Act
        current_user_path = "current_user.json"
        results = self.user_manager.current_user_id

        # Assert
        with open(current_user_path, "r") as file:
            current_user_data = json.load(file)
            
        self.assertIn("user_id", current_user_data)
        self.assertEqual(current_user_data["user_id"], results)

    def test_userManager_UserManager_delSessionFile(self):
        # Assemble
        account_name = "sotesty2@gmail.com"
        password = "example_passworD123"
        self.user_manager.register_and_login_user(account_name, password) 

        # Act
        with open(self.user_manager.SESSION_FILE, "w") as f:
          json.dump({"user_id": self.user_manager._current_user_id}, f)
          self.assertTrue(os.path.exists(self.user_manager.SESSION_FILE))

        if os.path.exists(UserManager.SESSION_FILE):
            os.remove(UserManager.SESSION_FILE)
        self.user_manager.save_session()

        # Assert
        del self.user_manager._current_user_id
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

    def test_userManager_register_and_login_user_returnWithSuccessMessage(self):
        # Assemble
        email = "test212@example.com"
        password = "testpassworD#123"

        # Act
        response = self.user_manager.register_and_login_user(email, password)

        # Assert
        self.assertEqual(response["status"], "success", msg=f"Registration failed: {response.get('message')}")

    def test_userManager_login_user_checkValidLoginBySuccessMessage(self):
        # Assemble
        email = "login_test4@example.com"
        password = "testlogiN#123"
        self.user_manager.register_and_login_user(email, password)
        result = self.user_manager.login_user(email, password)
        # Assert
        self.assertEqual(result["status"], "success")

    def test_userManager_login_user_checkInvalidLoginByIncorrectPassword(self):
        # Assemble
        email = "login_test5@example.com"
        password = "testlogiN#123"
        self.user_manager.register_and_login_user(email, password)
        # Act 
        result = self.user_manager.login_user(email, "wrongpassword")
        # Assert
        self.assertEqual(result["status"], "error")

    def teardown(self):
        self.user_manager.logout_user()

if __name__ == "__main__":
    unittest.main()
