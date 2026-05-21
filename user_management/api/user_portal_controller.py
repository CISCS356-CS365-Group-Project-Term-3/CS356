import user_management.api.user_portal_service as user_portal_service
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    user_name: str
    password: str

@app.post("/auth/login")
def login(login_details: LoginRequest):
    try:
        temp_token = user_portal_service.validate_login(login_details.model_dump())
        if temp_token:
            return {"access_token": temp_token, "token_type": "bearer"}
        else:
            return {"error": "Invalid Credentials, please try again"}
    except Exception as e:
        return {"error": f"Login failed: {str(e)}"}

@app.get("/auth/verify")
def verify(token: str):
    try:
        is_valid = user_portal_service.verify_token(token)
        if is_valid:
            user_id, user_role = user_portal_service.get_user_id_and_role(token)
            return {"user_id": user_id, "user_role": user_role}
        else:
            return {"error": "Invalid token"}
    except Exception as e:
        return {"error": f"Token verification failed: {str(e)}"}

