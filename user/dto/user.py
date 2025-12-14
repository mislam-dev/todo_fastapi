from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from user.models.user import UserRole, UserStatus


class UserResponseDto(BaseModel):
    id: UUID
    email: str
    status: UserStatus
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy objects
