import unittest
from py.models.page_manager import PageManager

# Navigate to project folder and run tests with 
#   `python -m unittest discover -s tests`

class TestPageManager(unittest.TestCase):
  # unittest runs setUp() before each test
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
                  result = self.page_manager.create_random_password(special_chars, length)
                  self.assertEqual(len(result), length, f"Failed for length {length}")

      # Test invalid lengths
          for length in invalid_lengths:
              with self.subTest(length=length):
                  with self.assertRaises(ValueError, msg=f"Should raise error for length {length}"):
                      self.page_manager.create_random_password(special_chars, length)

if __name__ == '__main__':
    unittest.main()