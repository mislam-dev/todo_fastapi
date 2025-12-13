from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.dto.todo import TodoCreateDto, TodoUpdateDto
from todo.models.todo import Todo
from user.models.user import User


class TodoService:
    def __init__(self, db: Session, user: User) -> None:
        self.db = db
        self.user = user

    def get_all(self):
        stmt = select(Todo).where(Todo.user_id == self.user.id)
        todo_data = self.db.scalars(stmt).all()
        return todo_data

    def create(self, data: TodoCreateDto):
        todo_data = data.model_dump()
        todo = Todo(
            **todo_data,
            user_id=self.user.id,
        )

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def get_single(self, id: UUID):
        stmt = select(Todo).where(
            Todo.id == id,
            Todo.user_id == self.user.id,
        )
        todo_data = self.db.scalars(stmt).first()

        if todo_data is None:
            raise HTTPException(
                status_code=404,
                detail="Todo not found!",
            )
        return todo_data

    def update(self, id: UUID, data: TodoUpdateDto):

        todo = self.get_single(id)

        updated_data = data.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(todo, key, value)

        self.db.commit()
        self.db.refresh(todo)
        return todo

    def remove(self, id: UUID):

        todo = self.get_single(id)
        self.db.delete(todo)
        self.db.commit()

        return None
