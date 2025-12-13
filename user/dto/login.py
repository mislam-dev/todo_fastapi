from pydantic import BaseModel, EmailStr


class LoginResponse(BaseModel):
    message: str
    access_token: str


# DTOs
class LoginDto(BaseModel):
    email: EmailStr
    password: str
