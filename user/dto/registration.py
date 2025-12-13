from pydantic import BaseModel, EmailStr


class RegistrationDto(BaseModel):
    email: EmailStr
    password: str
