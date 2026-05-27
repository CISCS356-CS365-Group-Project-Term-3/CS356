import user_management.api.user_portal_service as user_portal_service
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

