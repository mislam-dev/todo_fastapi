from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security.hash import Hash
from core.token import access_token
from user.dto.login import LoginDto
from user.dto.registration import RegistrationDto
from user.models.user import User


class UserService:
    invalid_user_exception = HTTPException(
        status_code=400,
        detail="Invalid user credentials",
    )

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()

    def create_new_user(self, data: RegistrationDto):

        if self.get_user_by_email(data.email):
            raise HTTPException(
                status_code=400,
                detail="Email is already exist",
            )

        hash_password = Hash.bcrypt(data.password)
        new_user = User(
            email=data.email,
            password=hash_password,
        )
        self.db.add(new_user)
        self.db.commit()

        self.db.refresh(new_user)
        return new_user

    def user_login(self, data: LoginDto):
        user = self.get_user_by_email(data.email)
        if not user:
            raise self.invalid_user_exception
        is_matched = Hash.verify(data.password, user.password)
        if not is_matched:
            raise self.invalid_user_exception
        token = access_token({"sub": user.email})
        return {
            "access_token": token,
            "token_type": "bearer",
        }
