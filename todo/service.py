from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import Uuid
from todo.dto.todo import TodoCreateDto, TodoUpdateDto
from sqlalchemy.orm import Session
from todo.models.todo import Todo


def getAll(
    db: Session,
    user_id: UUID,
):
    todo_data = db.query(Todo).filter(Todo.user_id == user_id).all()
    return todo_data


def create(
    db: Session,
    data: TodoCreateDto,
    user_id: UUID,
):
    todo_data = data.model_dump()
    todo = Todo(
        **todo_data,
        user_id=user_id,
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def getSingle(
    db: Session,
    id: UUID,
    user_id: UUID,
):
    todo_data = (
        db.query(Todo)
        .filter(
            Todo.id == id,
            Todo.user_id == user_id,
        )
        .first()
    )
    if todo_data is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found!",
        )
    return todo_data


def update(
    db: Session,
    id: UUID,
    data: TodoUpdateDto,
    user_id: UUID,
):

    todo = getSingle(db, id, user_id)

    if not todo.user_id == user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action!",
        )
    # update data
    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo


def remove(
    db: Session,
    id: UUID,
    user_id: UUID,
):

    todo = getSingle(db, id, user_id)

    if not todo.user_id == user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action!",
        )
    # update data
    db.delete(todo)
    db.commit()

    return True
