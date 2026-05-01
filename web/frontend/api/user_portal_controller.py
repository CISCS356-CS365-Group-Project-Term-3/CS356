from . import user_portal_service
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class LoginRequest(BaseModel):
    user_name: str
    password: str

@app.post("/auth/login")
def login(login_details: LoginRequest):
    """
        - 200: {"access_token": "jwt_token", "token_type": "bearer"}
        - 401: {"error": "Invalid Credentials, please try again"}
        - 500: {"error": "Login failed: error_message"}
    """
    try:
        temp_token = user_portal_service.validate_login(login_details.model_dump())
        if temp_token:
            return {"access_token": temp_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Credentials, please try again"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.get("/auth/verify")
def verify(authorisation: Optional[str] = Header(None)):
    """
        - 200: {"user_id": 1, "user_role": "admin"}
        - 401: {"error": "Unauthorised - missing or invalid token"}
        - 500: {"error": "Token verification failed: error_message"}
    """
    try:
        if not authorisation:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorised - missing Authorisation header"
            )

        # Parse Bearer token
        parts = authorisation.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorised - invalid Authorisation header format. Expected: Bearer <token>"
            )

        token = parts[1]

        # Verify token
        is_valid = user_portal_service.verify_token(token)
        if is_valid:
            user_id, user_role = user_portal_service.get_user_id_and_role(token)
            return {"user_id": user_id, "user_role": user_role}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorised - invalid or expired token"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token verification failed: {str(e)}"
        )


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirmRequest(BaseModel):
    token: str
    new_password: str


@app.post("/auth/reset_password")
def reset_password(request: PasswordResetRequest):
    """
        - 200: {"message": "If an account exists, a password reset link has been sent."}
        - 500: {"detail": "Unable to process password reset"}
    """
    try:
        user_portal_service.reset_password(request.email)
        return {"message": "If an account exists, a password reset link has been sent."}
    except Exception as e:
        print(f"Reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process password reset"
        )


@app.post("/auth/reset_password/confirm")
def confirm_reset_password(request: PasswordResetConfirmRequest):
    """
        - 200: {"message": "Password has been reset successfully."}
        - 400: {"detail": "Invalid or expired reset token"}
        - 500: {"detail": "Unable to process password reset"}
    """
    try:
        user_portal_service.confirm_password_reset(request.token, request.new_password)
        return {"message": "Password has been reset successfully."}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Confirm reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process password reset"
        )
