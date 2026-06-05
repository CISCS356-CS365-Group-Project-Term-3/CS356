from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open
import jwt
from datetime import datetime, timedelta
from user_management.api.user_portal_service import (
    validate_login,
    validate_credentials,
    get_user_info,
    verify_token,
    get_user_id_and_role,
    load_public_key,
    reset_password,
    confirm_password_reset,
    send_reset_email,
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

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_reset_password_db_connection_failure(self, mock_db):
        mock_db.return_value = None
        with self.assertRaises(Exception) as ctx:
            reset_password("user@example.com")
        self.assertIn("Database connection failed", str(ctx.exception))

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_reset_password_email_not_found(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result

        reset_password("notfound@example.com")

        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()

    @patch('user_management.api.user_portal_service.send_reset_email')
    @patch('user_management.api.user_portal_service.secrets.token_hex')
    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_reset_password_success(self, mock_db, mock_token_hex, mock_send_email):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = ("user@example.com",)
        mock_conn.execute.return_value = mock_result
        mock_token_hex.return_value = "abc123token"

        reset_password("user@example.com")

        mock_conn.commit.assert_called_once()
        mock_send_email.assert_called_once_with("user@example.com", "abc123token")
        mock_conn.close.assert_called_once()

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_confirm_password_reset_db_connection_failure(self, mock_db):
        mock_db.return_value = None
        with self.assertRaises(Exception) as ctx:
            confirm_password_reset("token", "newpass")
        self.assertIn("Database connection failed", str(ctx.exception))

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_confirm_password_reset_invalid_token(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result

        with self.assertRaises(ValueError) as ctx:
            confirm_password_reset("badtoken", "newpass")
        self.assertIn("Invalid or expired reset token", str(ctx.exception))
        mock_conn.close.assert_called_once()

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_confirm_password_reset_token_already_used(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = ("user@example.com", datetime.now() + timedelta(hours=1), True)
        mock_conn.execute.return_value = mock_result

        with self.assertRaises(ValueError) as ctx:
            confirm_password_reset("usedtoken", "newpass")
        self.assertIn("already been used", str(ctx.exception))
        mock_conn.close.assert_called_once()

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_confirm_password_reset_token_expired(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = ("user@example.com", datetime.now() - timedelta(hours=1), False)
        mock_conn.execute.return_value = mock_result

        with self.assertRaises(ValueError) as ctx:
            confirm_password_reset("expiredtoken", "newpass")
        self.assertIn("expired", str(ctx.exception))
        mock_conn.close.assert_called_once()

    @patch('user_management.api.user_portal_service.create_db_connection')
    def test_confirm_password_reset_success(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_result = MagicMock()
        mock_result.fetchone.return_value = ("user@example.com", datetime.now() + timedelta(hours=1), False)
        mock_conn.execute.return_value = mock_result

        confirm_password_reset("validtoken", "newpassword")

        self.assertEqual(mock_conn.execute.call_count, 3)
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_send_reset_email_missing_env_vars(self):
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(EnvironmentError) as ctx:
                send_reset_email("user@example.com", "token123")
            self.assertIn("GMAIL_SENDER", str(ctx.exception))

    @patch('user_management.api.user_portal_service.smtplib.SMTP_SSL')
    def test_send_reset_email_success(self, mock_smtp_cls):
        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__ = MagicMock(return_value=mock_server)
        mock_smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

        env = {"GMAIL_SENDER": "sender@gmail.com", "GMAIL_APP_PASSWORD": "apppass"}
        with patch.dict('os.environ', env):
            send_reset_email("user@example.com", "token123")

        mock_server.login.assert_called_once_with("sender@gmail.com", "apppass")
        mock_server.sendmail.assert_called_once()
