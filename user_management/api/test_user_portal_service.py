from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open
import jwt
from user_management.api.user_portal_service import (
    validate_login,
    validate_credentials,
    get_user_info,
    verify_token,
    get_user_id_and_role,
    load_public_key
)

class Test(TestCase):

    @patch('user_management.api.user_portal_service.validate_credentials')
    @patch('user_management.api.user_portal_service.get_user_info')
    @patch('user_management.api.user_portal_service.generate_token')
    def test_validate_login_success(self, mock_gen_token, mock_get_info, mock_validate_cred):
        mock_validate_cred.return_value = True
        mock_get_info.return_value = {"user_id": 1, "user_name": "test"}
        mock_gen_token.return_value = "fake_token"
        
        result = validate_login({"user_name": "test", "password": "password"})
        self.assertEqual(result, "fake_token")

    @patch('user_management.api.user_portal_service.validate_credentials')
    def test_validate_login_invalid_credentials(self, mock_validate_cred):
        mock_validate_cred.return_value = False
        result = validate_login({"user_name": "test", "password": "wrong_password"})
        self.assertFalse(result)

    @patch('user_management.api.user_portal_service.validate_credentials')
    @patch('user_management.api.user_portal_service.get_user_info')
    def test_validate_login_user_not_found(self, mock_get_info, mock_validate_cred):
        mock_validate_cred.return_value = True
        mock_get_info.return_value = None
        result = validate_login({"user_name": "test", "password": "password"})
        self.assertFalse(result)

    @patch('user_management.api.user_portal_service.validate_credentials')
    @patch('user_management.api.user_portal_service.get_user_info')
    @patch('user_management.api.user_portal_service.generate_token')
    def test_validate_login_token_error(self, mock_gen_token, mock_get_info, mock_validate_cred):
        mock_validate_cred.return_value = True
        mock_get_info.return_value = {"user_id": 1}
        mock_gen_token.side_effect = Exception("Token error")
        result = validate_login({"user_name": "test", "password": "password"})
        self.assertFalse(result)

    def test_validate_login_missing_key(self):
        result = validate_login({"user_name": "test"})
        self.assertFalse(result)

    @patch('user_management.api.user_portal_service.create_db_connection')
    @patch('bcrypt.checkpw')
    def test_validate_credentials_success(self, mock_bcrypt, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = ("hashed_password",)
        mock_conn.execute.return_value = mock_result
        mock_bcrypt.return_value = True
        
        result = validate_credentials("user", "pass")
        self.assertTrue(result)
        mock_conn.close.assert_called_once()

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_validate_credentials_user_not_found(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result
        
        result = validate_credentials("user", "pass")
        self.assertFalse(result)

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_validate_credentials_db_error(self, mock_db):
        mock_db.return_value = None
        result = validate_credentials("user", "pass")
        self.assertFalse(result)

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_get_user_info_success(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = (1, "user", "email", "role")
        mock_conn.execute.return_value = mock_result
        
        result = get_user_info("user")
        self.assertEqual(result["user_id"], 1)
        self.assertEqual(result["user_role"], "role")

    @patch('user_management.api.user_portal_service.load_public_key')
    @patch('jwt.decode')
    def test_verify_token_success(self, mock_jwt_decode, mock_load_key):
        mock_load_key.return_value = "fake_key"
        result = verify_token("token")
        self.assertTrue(result)

    @patch('user_management.api.user_portal_service.load_public_key')
    @patch('jwt.decode')
    def test_verify_token_expired(self, mock_jwt_decode, mock_load_key):
        mock_load_key.return_value = "fake_key"
        mock_jwt_decode.side_effect = jwt.ExpiredSignatureError()
        result = verify_token("token")
        self.assertFalse(result)

    @patch('user_management.api.user_portal_service.load_public_key')
    @patch('jwt.decode')
    def test_get_user_id_and_role_success(self, mock_jwt_decode, mock_load_key):
        mock_load_key.return_value = "fake_key"
        mock_jwt_decode.return_value = {"user_id": 123, "user_role": "admin"}
        user_id, role = get_user_id_and_role("token")
        self.assertEqual(user_id, 123)
        self.assertEqual(role, "admin")

    @patch("builtins.open", new_callable=mock_open, read_data="ssh-rsa AAAAB3Nza...")
    @patch("cryptography.hazmat.primitives.serialization.load_ssh_public_key")
    def test_load_public_key_success(self, mock_load_ssh, mock_file):
        mock_load_ssh.return_value = "public_key_object"
        result = load_public_key()
        self.assertEqual(result, "public_key_object")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_public_key_not_found(self, mock_file):
        result = load_public_key()
        self.assertIsNone(result)
