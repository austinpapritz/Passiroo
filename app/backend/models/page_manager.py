import random
import string

class PageManager:
    def generate_random_password(self, special_chars, length):
        if length < 8 or length > 16:
            raise ValueError("Password length must be between 8 and 16 characters.")

        # Ensure special_chars contains unique characters only
        special_chars = "".join(set(special_chars))

        # Check if the length is sufficient to include all types of characters
        if length < len(special_chars) + 3:
            raise ValueError("Password length is too short to include all special characters and at least one lowercase, one uppercase, and one digit.")

        # Lists of character types
        lower = list(string.ascii_lowercase)
        upper = list(string.ascii_uppercase)
        digits = list(string.digits)

        # Create lists to ensure at least one of each required type is used
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits)
        ]

        # Add one of each special character to the password
        password.extend(list(special_chars))

        # Fill the rest of the password length with random choices from all character pools
        all_chars = lower + upper + digits + list(special_chars)
        remaining_length = length - len(password)
        password.extend(random.choices(all_chars, k=remaining_length))

        # Shuffle the password list to ensure randomness
        random.shuffle(password)

        # Return the password as a string
        return "".join(password)