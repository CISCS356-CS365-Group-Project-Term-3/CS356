from unittest import TestCase
from user_management.authentication.token_generation import main
from unittest.mock import patch, mock_open
from user_management.authentication.token_generation import load_key

class Test(TestCase):
    def test_generate_token_success(self):
        json = {"user_id": 1, "user_name": "test", "user_email": "", "user_role": "admin"}
        token = main(json)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertEqual(len(token.split('.')), 3)
        
    def test_generate_token_none_json(self):
        json = None
        with self.assertRaises(ValueError):
            main(json)

    def test_generate_token_missing_key(self):
        json = {"user_id": 1}  # missing user_name, user_email, user_role
        result = main(json)
        self.assertIsNone(result)

    def test_generate_token_no_key(self):
        json = {"user_id": 1, "user_name": "test", "user_email": "", "user_role": "admin"}
        with patch("user_management.authentication.token_generation.load_key", return_value=None):
            with self.assertRaises(Exception, msg="Private key file not found or invalid."):
                main(json)

    def test_load_key_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_key()
            self.assertIsNone(result)

    def test_load_key_invalid_key(self):
        with patch("builtins.open", mock_open(read_data="not-a-real-key")):
            result = load_key()
            self.assertIsNone(result)