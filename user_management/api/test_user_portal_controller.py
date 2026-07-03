import asyncio
import json
from unittest import TestCase
from unittest.mock import patch

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError

from user_management.api.user_portal_controller import (
    error_response,
    http_exception_handler,
    login,
    LoginRequest,
    register,
    RegisterUser,
    validation_exception_handler,
)


class TestUserPortalController(TestCase):

    def assert_error_response(self, response, expected_status_code, expected_message):
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(
            json.loads(response.body.decode("utf-8")),
            error_response(expected_status_code, expected_message)
        )

    def valid_register_details(self, **overrides):
        details = {
            "user_name": "test",
            "password": "password123",
            "user_email": "test@example.com",
            "confirm_password": "password123",
            "user_role": "user"
        }
        details.update(overrides)
        return RegisterUser(**details)

    def test_validation_error_returns_400(self):
        validation_error = RequestValidationError([
            {
                "loc": ("body", "password"),
                "msg": "Field required",
                "type": "missing"
            }
        ])

        response = asyncio.run(
            validation_exception_handler(None, validation_error)
        )

        self.assert_error_response(
            response,
            status.HTTP_400_BAD_REQUEST,
            "Invalid request data"
        )

    @patch("user_management.api.user_portal_controller.user_portal_service.validate_login")
    def test_invalid_login_returns_401(self, mock_validate_login):
        mock_validate_login.return_value = False

        with self.assertRaises(HTTPException) as ctx:
            login(LoginRequest(user_name="test", password="wrong-password"))

        response = asyncio.run(http_exception_handler(None, ctx.exception))

        self.assert_error_response(
            response,
            status.HTTP_401_UNAUTHORIZED,
            "Invalid username or password"
        )

    def test_forbidden_access_returns_403(self):
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )

        response = asyncio.run(http_exception_handler(None, exception))

        self.assert_error_response(
            response,
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to access this resource"
        )

    def test_missing_user_returns_404(self):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

        response = asyncio.run(http_exception_handler(None, exception))

        self.assert_error_response(
            response,
            status.HTTP_404_NOT_FOUND,
            "User not found"
        )

    @patch("user_management.api.user_portal_controller.user_portal_service.validate_login")
    def test_internal_errors_return_safe_message(self, mock_validate_login):
        mock_validate_login.side_effect = Exception("postgresql://admin:secret@localhost")

        with self.assertRaises(HTTPException) as ctx:
            login(LoginRequest(user_name="test", password="password"))

        response = asyncio.run(http_exception_handler(None, ctx.exception))
        body = response.body.decode("utf-8")

        self.assert_error_response(
            response,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Unable to process login request"
        )
        self.assertNotIn("postgresql", body)
        self.assertNotIn("secret", body)

    @patch("user_management.api.user_portal_controller.user_portal_service.create_user")
    @patch("user_management.api.user_portal_controller.user_portal_service.get_user_info")
    def test_register_success(self, mock_get_user_info, mock_create_user):
        mock_get_user_info.return_value = None
        mock_create_user.return_value = True

        result = register(self.valid_register_details())

        self.assertEqual(result, {"message": "Account created successfully"})
        mock_get_user_info.assert_called_once_with("test")
        mock_create_user.assert_called_once_with(
            "test",
            "test@example.com",
            "user",
            "password123"
        )

    @patch("user_management.api.user_portal_controller.user_portal_service.create_user")
    @patch("user_management.api.user_portal_controller.user_portal_service.get_user_info")
    def test_register_password_mismatch_returns_400(
        self,
        mock_get_user_info,
        mock_create_user
    ):
        with self.assertRaises(HTTPException) as ctx:
            register(self.valid_register_details(confirm_password="different"))

        response = asyncio.run(http_exception_handler(None, ctx.exception))

        self.assert_error_response(
            response,
            status.HTTP_400_BAD_REQUEST,
            "Passwords do not match"
        )
        mock_get_user_info.assert_not_called()
        mock_create_user.assert_not_called()

    @patch("user_management.api.user_portal_controller.user_portal_service.create_user")
    @patch("user_management.api.user_portal_controller.user_portal_service.get_user_info")
    def test_register_invalid_role_returns_400(
            self,
            mock_get_user_info,
            mock_create_user
    ):
        with self.assertRaises(HTTPException) as ctx:
            register(self.valid_register_details(user_role="invalid_role"))

        response = asyncio.run(http_exception_handler(None, ctx.exception))

        self.assert_error_response(
            response,
            status.HTTP_400_BAD_REQUEST,
            "User role is not valid"
        )
        mock_get_user_info.assert_not_called()
        mock_create_user.assert_not_called()

    @patch("user_management.api.user_portal_controller.user_portal_service.create_user")
    @patch("user_management.api.user_portal_controller.user_portal_service.get_user_info")
    def test_register_existing_username_returns_409(
        self,
        mock_get_user_info,
        mock_create_user
    ):
        mock_get_user_info.return_value = {"user_id": 1, "user_name": "test"}

        with self.assertRaises(HTTPException) as ctx:
            register(self.valid_register_details())

        response = asyncio.run(http_exception_handler(None, ctx.exception))

        self.assert_error_response(
            response,
            status.HTTP_409_CONFLICT,
            "Username already exists"
        )
        mock_get_user_info.assert_called_once_with("test")
        mock_create_user.assert_not_called()

    @patch("user_management.api.user_portal_controller.user_portal_service.create_user")
    @patch("user_management.api.user_portal_controller.user_portal_service.get_user_info")
    def test_register_create_user_failure_returns_500(
        self,
        mock_get_user_info,
        mock_create_user
    ):
        mock_get_user_info.return_value = None
        mock_create_user.return_value = False

        with self.assertRaises(HTTPException) as ctx:
            register(self.valid_register_details())

        response = asyncio.run(http_exception_handler(None, ctx.exception))

        self.assert_error_response(
            response,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "User could not be created"
        )
        mock_get_user_info.assert_called_once_with("test")
        mock_create_user.assert_called_once_with(
            "test",
            "test@example.com",
            "user",
            "password123"
        )

    @patch("user_management.api.user_portal_controller.user_portal_service.log_audit_action")
    @patch("user_management.api.user_portal_controller.user_portal_service.update_user_role")
    @patch("user_management.api.user_portal_controller.user_portal_service.get_user_id_and_role")
    @patch("user_management.api.user_portal_controller.user_portal_service.verify_token")
    @patch("user_management.api.user_portal_controller.get_current_token")
    def test_admin_update_user_role_logs_audit_action(
            self,
            mock_get_token,
            mock_verify,
            mock_get_id_role,
            mock_update,
            mock_log_audit
    ):
        mock_get_token.return_value = "valid_token"
        mock_verify.return_value = True
        mock_get_id_role.return_value = (1, "admin")
        mock_update.return_value = True

        from user_management.api.user_portal_controller import admin_update_user_role

        result = admin_update_user_role(42, "moderator")

        self.assertEqual(result, {"message": "User with ID 42 updated to role moderator successfully"})
        mock_log_audit.assert_called_once_with(1, 42, "UPDATE_ROLE_MODERATOR")


    @patch("user_management.api.user_portal_controller.user_portal_service.log_audit_action")
    @patch("user_management.api.user_portal_controller.user_portal_service.delete_user")
    @patch("user_management.api.user_portal_controller.user_portal_service.get_user_id_and_role")
    @patch("user_management.api.user_portal_controller.user_portal_service.verify_token")
    @patch("user_management.api.user_portal_controller.get_current_token")
    def test_admin_delete_user_logs_audit_action(
            self,
            mock_get_token,
            mock_verify,
            mock_get_id_role,
            mock_delete,
            mock_log_audit
    ):
        mock_get_token.return_value = "valid_token"
        mock_verify.return_value = True
        mock_get_id_role.return_value = (1, "admin")

        from user_management.api.user_portal_controller import admin_delete_user

        result = admin_delete_user(42)

        self.assertEqual(result, {"message": "User with ID 42 deleted successfully"})
        mock_log_audit.assert_called_once_with(1, 42, "DELETE_USER")