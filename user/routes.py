from fastapi import APIRouter
from fastapi import Depends, HTTPException
from h11 import Data
from sqlalchemy.orm import Session
from core.dependencies import auth
from database.database import db_instance
from user.dto.user import UserResponseDto
from user.models.user import User
from user.dto.login import LoginDto, LoginResponse
from user.dto.registration import RegistrationDto
from user.service import create_new_user, get_user_by_email, user_login
from core.dependencies.auth import auth

router = APIRouter()


@router.post("/login")
def login(data: LoginDto, db: Session = Depends(db_instance.get_db)):
    return user_login(db, data)


@router.post("/register")
def register(
    data: RegistrationDto,
    db: Session = Depends(db_instance.get_db),
):
    db_user = get_user_by_email(db, data.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already exist",
        )

    new_user = create_new_user(db, data)
    return {
        "message": "user registered successfully",
        "user_id": new_user.id,
    }


@router.get("/me", response_model=UserResponseDto)
def me(
    db: Session = Depends(db_instance.get_db),
    current_user: User = Depends(auth.get_current_user),
):
    return current_user
