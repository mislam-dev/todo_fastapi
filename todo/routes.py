from datetime import datetime
from tokenize import Triple
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import true
from core.dependencies.auth import auth
from todo.dto import todo
from todo.dto.todo import TodoCreateDto, TodoResponseDto, TodoUpdateDto
from user.models.user import User
from todo.service import create, getSingle, getAll, remove, update
from sqlalchemy.orm import Session
from database.database import db_instance

router = APIRouter()


@router.get("/", response_model=List[TodoResponseDto])
def getAll_todos(
    db: Session = Depends(db_instance.get_db),
    current_user: User = Depends(auth.get_current_user),
):
    allTodos = getAll(db, current_user.id)

    return allTodos


@router.get("/{todo_id}", response_model=TodoResponseDto)
def get_todo(
    todo_id: UUID,
    db: Session = Depends(db_instance.get_db),
    current_user: User = Depends(auth.get_current_user),
):
    allTodos = getSingle(db, todo_id, current_user.id)

    return allTodos


@router.post("/", response_model=TodoResponseDto)
def create_todo(
    data: TodoCreateDto,
    db: Session = Depends(db_instance.get_db),
    current_user: User = Depends(auth.get_current_user),
):
    new_todo = create(db, data, current_user.id)

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
    db: Session = Depends(db_instance.get_db),
    current_user: User = Depends(auth.get_current_user),
):
    updated = update(db, todo_id, data, current_user.id)

    return updated


@router.delete("/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    db: Session = Depends(db_instance.get_db),
    current_user: User = Depends(auth.get_current_user),
):
    remove(db, todo_id, current_user.id)
    return True
