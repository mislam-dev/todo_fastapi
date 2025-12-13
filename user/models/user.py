import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


# enums
class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    verified = "verified"
    suspended = "suspended"


# models
class User(Base):

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[Optional[UserStatus]] = mapped_column(
        SQLEnum(UserStatus), default=UserStatus.active
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
