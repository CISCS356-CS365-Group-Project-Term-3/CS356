from . import user_portal_service
from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional
from contextlib import asynccontextmanager
import configparser
import os

_PROPERTIES_PATH = os.path.join(os.path.dirname(__file__), '..', 'user.properties')
_SECTION = 'tokens'
_SESSION_SECTION = 'session'


def save_token(user_name: str, token: str) -> None:
    config = configparser.RawConfigParser()
    config.read(_PROPERTIES_PATH)
    if not config.has_section(_SECTION):
        config.add_section(_SECTION)
    config.set(_SECTION, user_name, token)
    if not config.has_section(_SESSION_SECTION):
        config.add_section(_SESSION_SECTION)
    config.set(_SESSION_SECTION, 'token', token)
    with open(_PROPERTIES_PATH, 'w') as f:
        config.write(f)


def get_current_token() -> str | None:
    config = configparser.RawConfigParser()
    config.read(_PROPERTIES_PATH)
    return config.get(_SESSION_SECTION, 'token', fallback=None)


def _reset_properties() -> None:
    with open(_PROPERTIES_PATH, 'w') as f:
        f.write(f'[{_SECTION}]\n\n[{_SESSION_SECTION}]\n')


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    _reset_properties()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterUser(BaseModel):
    user_name: str
    password: str
    user_email: EmailStr
    confirm_password: str
    user_role: str

@app.post("/auth/register")
def register(register_details: RegisterUser):
    try:
        print("\n" + "="*60)
        print(f"REGISTRATION REQUEST: {register_details.user_name}")
        print("="*60)
        
        if register_details.password != register_details.confirm_password:
            print("[FAIL] Password mismatch")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        allowed_roles = ["user", "admin"]

        if register_details.user_role not in allowed_roles:
            print(f"[FAIL] Invalid role: {register_details.user_role}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User role is not valid"
            )

        # Check if username already exists
        print(f"[CHECK] Username availability: {register_details.user_name}")
        existing_user = user_portal_service.get_user_info(register_details.user_name)
        if existing_user is not None:
            print(f"[FAIL] Username already taken: {register_details.user_name}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This username is already taken"
            )
        print("[OK] Username available")

        # Check if email already exists
        print(f"[CHECK] Email availability: {register_details.user_email}")
        if user_portal_service.user_email_exists(register_details.user_email):
            print(f"[FAIL] Email already registered: {register_details.user_email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered"
            )
        print("[OK] Email available")

        # Create user
        print("[ACTION] Creating user...")
        result = user_portal_service.create_user(
            register_details.user_name,
            register_details.user_email,
            register_details.user_role,
            register_details.password
        )

        # Handle response - could be dict or bool
        if isinstance(result, dict):
            if result.get("success"):
                print("[SUCCESS] User created successfully")
                return {"message": "Account created successfully"}
            else:
                error_msg = result.get("error", "Unable to create user account")
                print(f"[FAIL] User creation failed: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
        elif not result:
            print("[FAIL] User creation failed (returned False)")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to create user account"
            )

        print("[SUCCESS] Registration complete")
        return {"message": "Account created successfully"}
        
    except HTTPException as e:
        print(f"[EXCEPTION] HTTPException: {e.detail}")
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process registration"
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
            save_token(login_details.user_name, temp_token)
            return {"access_token": temp_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process login request"
        )

@app.get("/auth/verify")
def verify(authorization: Optional[str] = Header(None)):
    """
        - 200: {"user_id": 1, "user_role": "admin"}
        - 401: {"error": {"status_code": 401, "message": "Unauthorized - missing or invalid token"}}
        - 500: {"error": {"status_code": 500, "message": "Unable to verify token"}}
    """
    try:
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - missing or invalid token"
            )

        # Parse Bearer token
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - missing or invalid token"
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
                detail="Unauthorized - missing or invalid token"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to verify token"
        )


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirmRequest(BaseModel):
    token: str
    new_password: str


class UserInfoRequest(BaseModel):
    user_name: str


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

@app.get("/auth/users")
def admin_list_users():
    token = get_current_token()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No active session - please log in")
    if not user_portal_service.verify_token(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session token is invalid or expired")
    _, role = user_portal_service.get_user_id_and_role(token)
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user_portal_service.get_all_users()


@app.post("/auth/users/delete/{user_id}")
def admin_delete_user(user_id: str):
    try:
        token = get_current_token()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No active session - please log in")
        if not user_portal_service.verify_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session token is invalid or expired")

        actor_id, user_role = user_portal_service.get_user_id_and_role(token)

        if user_role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

        try:
            user_portal_service.log_audit_action(actor_id, user_id, "DELETE_USER")
            user_portal_service.delete_user(user_id)
            return {"message": f"User with ID {user_id} deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting user: {str(e)}")
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/users/me")
def get_user_details(authorization: Optional[str] = Header(None)):
    try:
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - missing or invalid token"
            )

        # Parse Bearer token
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - missing or invalid token"
            )

        token = parts[1]

        # Verify token
        is_valid = user_portal_service.verify_token(token)
        if is_valid:
            user_id, user_role, user_name, user_email = user_portal_service.get_user_details(token)
            return {"user_id": user_id, "user_name": user_name, "user_role": user_role, "user_email": user_email}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - missing or invalid token"
            )
    except HTTPException:
        raise
    except Exception:
        print("Token verification error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to verify token"
        )

@app.post("/auth/users/update/{user_id}/{role:path}")
def admin_update_user_role(user_id: str, role: str):
    try:
        token = get_current_token()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No active session - please log in")
        if not user_portal_service.verify_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session token is invalid or expired")

        actor_id, user_role = user_portal_service.get_user_id_and_role(token)

        if user_role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

        updated = user_portal_service.update_user_role(user_id, role)
        if updated:
            user_portal_service.log_audit_action(actor_id, user_id, f"UPDATE_ROLE_{role.upper()}")
            return {"message": f"User with ID {user_id} updated to role {role} successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating user role: {str(e)}")


@app.get("/health")
def health():
    return {"status": "ok"}
