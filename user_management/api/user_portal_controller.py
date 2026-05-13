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

