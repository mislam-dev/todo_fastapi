import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sqlalchemy import UUID, DateTime, ForeignKey, String, create_engine, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

app = FastAPI()


# alchemy class config
class Database:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close

    def create_table(self, base: type[DeclarativeBase]):
        base.metadata.create_all(bind=self.engine)


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/todo"
db_instance = Database(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase):
    pass


# enums
class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    verified = "verified"
    suspended = "suspended"


class TodoStatus(str, Enum):
    todo = "todo"
    progress = "progress"
    completed = "completed"
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


db_instance.create_table(Base)


# responses
class LoginResponse(BaseModel):
    message: str
    access_token: str


# DTOs
class LoginRequestBody(BaseModel):
    email: EmailStr
    password: str


class TodoCreateDto(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdateDto(TodoCreateDto):
    pass


@app.get("/")
def get_root():
    return {"message": "Server is running!"}


@app.get("/todos")
def get_all_todos():
    return {"message": "return all todos"}


@app.post(
    "/todos",
)
def create_todo(data: TodoCreateDto):
    todoData = {
        "id": "1",
        "user_id": "1",
        "title": data.title,
        "description": data.description,
        "created_at": "current date",
    }
    return todoData


@app.patch("/todos/{todo_id}")
def update_todo(todo_id: str):
    return {"message": "update single todo", "id": todo_id}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    return {"message": "delete single todo"}


@app.post(
    "/auth/login",
)
def login(data: LoginRequestBody):
    return {"message": "user login", "access_token": "data"}


@app.post("/auth/register")
def register():
    return {"message": "user register"}
