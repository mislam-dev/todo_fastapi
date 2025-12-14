from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import RoleChecker
from core.dependencies.auth import auth
from database.database import db_instance
from user.dto import user
from user.dto.login import LoginDto
from user.dto.registration import RegistrationDto
from user.dto.user import UserResponseDto
from user.models.user import User, UserRole
from user.service import UserService
from core.dependencies.RoleChecker import RoleChecker

router = APIRouter()


def get_user_service(db: Session = Depends(db_instance.get_db)) -> UserService:
    return UserService(db)


@router.post("/login")
def login(data: LoginDto, user_service: UserService = Depends(get_user_service)):
    return user_service.user_login(data)


@router.post("/register")
def register(
    data: RegistrationDto, user_service: UserService = Depends(get_user_service)
):
    new_user = user_service.create_new_user(data)
    return {
        "message": "user registered successfully",
        "user_id": new_user.id,
    }


@router.get("/me", response_model=UserResponseDto)
def me(current_user: User = Depends(auth.get_current_user)):
    return current_user


@router.get(
    "/users",
    response_model=List[UserResponseDto],
    dependencies=[Depends(RoleChecker([UserRole.MODERATOR, UserRole.ADMIN]))],
)
def all_user(
    auth: bool = Depends(auth.authenticate),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_all_users()
