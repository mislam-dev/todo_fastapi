from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies.auth import auth
from database.database import db_instance
from todo.dto.todo import TodoCreateDto, TodoResponseDto, TodoUpdateDto
from todo.service import TodoService
from user.models.user import User

router = APIRouter()


def get_todo_service(
    db: Session = Depends(db_instance.get_db),
    user: User = Depends(auth.get_current_user),
) -> TodoService:
    return TodoService(db, user)


@router.get("/", response_model=List[TodoResponseDto])
def getAll_todos(
    todo_service: TodoService = Depends(get_todo_service),
):
    allTodos = todo_service.get_all()
    return allTodos


@router.get("/{todo_id}", response_model=TodoResponseDto)
def get_todo(
    todo_id: UUID,
    todo_service: TodoService = Depends(get_todo_service),
):
    singleTodo = todo_service.get_single(
        todo_id,
    )
    return singleTodo


@router.post("/", response_model=TodoResponseDto)
def create_todo(
    data: TodoCreateDto,
    todo_service: TodoService = Depends(get_todo_service),
):
    new_todo = todo_service.create(
        data,
    )

    if not new_todo:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server error!",
        )
    return new_todo


@router.patch("/{todo_id}/", response_model=TodoResponseDto)
def update_todo(
    todo_id: UUID,
    data: TodoUpdateDto,
    todo_service: TodoService = Depends(get_todo_service),
):
    updated = todo_service.update(
        todo_id,
        data,
    )

    return updated


@router.delete("/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    todo_service: TodoService = Depends(get_todo_service),
):
    todo_service.remove(
        todo_id,
    )
    return None
