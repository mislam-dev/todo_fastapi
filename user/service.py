import email
from token import tok_name
from tokenize import TokenError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.token import access_token
from core.security.hash import Hash
from user.dto.login import LoginDto
from user.dto.registration import RegistrationDto
from user.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_new_user(db: Session, data: RegistrationDto):

    hash_password = Hash.bcrypt(data.password)
    new_user = User(
        email=data.email,
        password=hash_password,
    )
    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user


def user_login(db: Session, data: LoginDto):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid user credentials",
        )
    is_matched = Hash.verify(data.password, user.password)
    if not is_matched:
        raise HTTPException(
            status_code=400,
            detail="Invalid user credentials",
        )
    token = access_token(
        {
            "sub": user.email,
        }
    )
    return {
        "token": token,
        "token_type": "bearer",
    }
