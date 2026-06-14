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
    validation_exception_handler,
)


class TestUserPortalController(TestCase):
    def assert_error_response(self, response, expected_status_code, expected_message):
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(
            json.loads(response.body.decode("utf-8")),
            error_response(expected_status_code, expected_message)
        )

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
