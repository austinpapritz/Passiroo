import unittest
import string
from app.backend.models.page_manager import PageManager

# Navigate to project folder and run tests with 
#   `python -m unittest discover -s tests`

class TestPageManager(unittest.TestCase):
  def setUp(self):
      self.page_manager = PageManager()

  def test_pageManager_createRandomPassword_outputMatchesPasswordLengthForValidLengths(self):
      # Assemble
          valid_lengths = [8, 12, 16]
          invalid_lengths = [5, 25]
          special_chars = "!@#"

      # Test valid lengths
          for length in valid_lengths:
              with self.subTest(length=length):
                  result = self.page_manager.generate_random_password(special_chars, length)
                  self.assertEqual(len(result), length, f"Failed for length {length}")

      # Test invalid lengths
          for length in invalid_lengths:
              with self.subTest(length=length):
                  with self.assertRaises(ValueError, msg=f"Should raise error for length {length}"):
                      self.page_manager.generate_random_password(special_chars, length)
                      
  def test_pageManager_createRandomPassword_outputContainsCorrectSpecialChars(self):
      # Assemble
          special_chars1 = "!@#"
          special_chars2 = "!-."
          special_chars3 = "@%&$"
          length = 12
          
      # Act
          result1 = self.page_manager.generate_random_password(special_chars1, length)
          result2 = self.page_manager.generate_random_password(special_chars2, length)
          result3 = self.page_manager.generate_random_password(special_chars3, length)

      # Assert
          for char in special_chars1:
              with self.subTest(char=char):
                  self.assertIn(char, result1, f"Special character {char} not found in password1")
          for char in special_chars2:
              with self.subTest(char=char):
                  self.assertIn(char, result2, f"Special character {char} not found in password2")
          for char in special_chars3:
              with self.subTest(char=char):
                  self.assertIn(char, result3, f"Special character {char} not found in password3")
                  
  def test_pageManager_createRandomPassword_outputContainsLowerUpperAndDigit(self):
      # Assemble
          special_chars = "@%&$-."
          length = 12
          lower = set(string.ascii_lowercase)
          upper = set(string.ascii_uppercase)
          digits = set(string.digits)
          
      # Act
          results = [self.page_manager.generate_random_password(special_chars, length) for _ in range(3)]

      # Assert
          for i, result in enumerate(results, 1):
            self.assertTrue(any(c in result for c in lower), f"Lowercase character not found in result {i}")
            self.assertTrue(any(c in result for c in upper), f"Uppercase character not found in result {i}")
            self.assertTrue(any(c in result for c in digits), f"Digit not found in result {i}")
            
  def test_pageManager_createRandomPassword_outputIsRandom(self):
      # Assemble
          special_chars = "@%&$-."
          length = 12

      # Act
          results = [self.page_manager.generate_random_password(special_chars, length) for _ in range(10)]

      # Assert
          seen_passwords = set()
          for i, result in enumerate(results, 1):
              # Check if the password is already in the set
              self.assertNotIn(result, seen_passwords, f"Password {i} was found more than once.")
              seen_passwords.add(result)  # Add the password to the set

if __name__ == '__main__':
    unittest.main()