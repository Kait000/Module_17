from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateUser, UpdateUser
from app.models.user import User
from app.models.task import Task
from slugify import slugify


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    """Возвращает список всех пользователей"""
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    """Возвращает пользователя по id"""
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')
    return user


@router.get('/user_id/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id_: int):
    """Возвращает список задач для пользователя по id"""
    if not db.scalar(select(User).where(User.id == user_id_)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')

    if not db.scalar(select(Task).where(Task.user_id == user_id_)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Task was not found')

    tasks = db.scalars(select(Task).where(Task.user_id == user_id_)).all()
    return tasks


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], add_user: CreateUser):
    """Создает нового пользователя"""
    if db.scalar(select(User).where(User.username == add_user.username)):
        return {'Message': f'User {add_user.username} is already exists '}

    db.execute(insert(User).values(username=add_user.username,
                                   firstname=add_user.firstname,
                                   lastname=add_user.lastname,
                                   age=add_user.age,
                                   slug=slugify(add_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], update_user_: UpdateUser, user_id: int):
    """Обновляет данные пользователя по id"""
    update_new_user = db.scalar(select(User).where(User.id == user_id))
    if not update_new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')

    db.execute(update(User).where(User.id == user_id).values(firstname=update_user_.firstname,
                                                             lastname=update_user_.lastname,
                                                             age=update_user_.age))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], del_id: int):
    """Удаляет пользователя по id"""
    del_user = db.scalar(select(User).where(User.id == del_id))
    if not del_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')

    db.execute(delete(User).where(User.id == del_id))
    db.execute(delete(Task).where(Task.user_id == del_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User and tasks was deleted!'}
