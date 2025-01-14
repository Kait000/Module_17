from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateTask, UpdateTask
from app.models.user import User
from app.models.task import Task
from slugify import slugify


router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    """Возвращает список всех задач"""
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    """Возвращает список задач по id"""
    task = db.scalar(select(Task).where(Task.id == task_id))
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Task was not found')
    return task


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], add_task: CreateTask, user_id_: int):
    """Создает новое задание для пользователя user_id"""
    if not db.scalar(select(User).where(User.id == user_id_)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')

    if db.scalar(select(Task).where(Task.title == add_task.title)):
        return {'Message': f'Task {add_task.title} is already exists '}

    db.execute(insert(Task).values(title=add_task.title,
                                   content=add_task.content,
                                   priority=add_task.priority,
                                   user_id=user_id_,
                                   slug=slugify(add_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], update_task_: UpdateTask, task_id: int):
    """Обновляет данные задачи по id"""
    update_new_task = db.scalar(select(Task).where(Task.id == task_id))
    if not update_new_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Task was not found')

    db.execute(update(Task).where(Task.id == task_id).values(title=update_task_.title,
                                                             content=update_task_.content,
                                                             priority=update_task_.priority))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'}


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], del_id: int):
    """Удаляет задачу по id"""
    del_task = db.scalar(select(Task).where(Task.id == del_id))
    if not del_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Task was not found')

    db.execute(delete(Task).where(Task.id == del_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task was deleted!'}
