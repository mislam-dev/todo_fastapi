from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from todo.models.todo import TodoStatus


class TodoCreateDto(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdateDto(TodoCreateDto):
    pass


class TodoResponseDto(BaseModel):
    id: UUID
    title: str
    description: str
    status: TodoStatus
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy objects
