import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import UUID, DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class TodoStatus(str, Enum):
    todo = "todo"
    progress = "progress"
    completed = "completed"
    suspended = "suspended"


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    status: Mapped[Optional[TodoStatus]] = mapped_column(
        SQLEnum(TodoStatus), default=TodoStatus.todo
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
