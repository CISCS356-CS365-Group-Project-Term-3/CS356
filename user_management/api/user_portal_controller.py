from . import user_portal_service
from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional

app = FastAPI()


def error_response(status_code: int, message: str):
    return {
        "error": {
            "status_code": status_code,
            "message": message
        }
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, _exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response(
            status.HTTP_400_BAD_REQUEST,
            "Invalid request data"
        )
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
    message = exc.detail if isinstance(exc.detail, str) else "Unable to process request"

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.status_code, message)
    )


class LoginRequest(BaseModel):
    user_name: str
    password: str

@app.post("/auth/login")
def login(login_details: LoginRequest):
    """
        - 200: {"access_token": "jwt_token", "token_type": "bearer"}
        - 400: {"error": {"status_code": 400, "message": "Invalid request data"}}
        - 401: {"error": {"status_code": 401, "message": "Invalid username or password"}}
        - 500: {"error": {"status_code": 500, "message": "Unable to process login request"}}
    """
    try:
        temp_token = user_portal_service.validate_login(login_details.model_dump())
        if temp_token:
            return {"access_token": temp_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
    except HTTPException:
        raise
    except Exception:
        print("Login error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process login request"
        )

@app.get("/auth/verify")
def verify(authorisation: Optional[str] = Header(None)):
    """
        - 200: {"user_id": 1, "user_role": "admin"}
        - 401: {"error": {"status_code": 401, "message": "Unauthorised - missing or invalid token"}}
        - 500: {"error": {"status_code": 500, "message": "Unable to verify token"}}
    """
    try:
        if not authorisation:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorised - missing or invalid token"
            )

        # Parse Bearer token
        parts = authorisation.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorised - missing or invalid token"
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
                detail="Unauthorised - missing or invalid token"
            )
    except HTTPException:
        raise
    except Exception:
        print("Token verification error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to verify token"
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
    except Exception:
        print("Reset error")
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
    except Exception:
        print("Confirm reset error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process password reset"
        )
