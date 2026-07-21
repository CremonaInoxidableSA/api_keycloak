from pydantic import BaseModel

class ResetPasswordRequest(BaseModel):
    password: str
    password_confirmation: str
