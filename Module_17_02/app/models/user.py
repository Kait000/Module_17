from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.backend.db import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)  # целое число, первичный ключ, с индексом.
    username = Column(String)                           # строка
    firstname = Column(String)                          # строка
    lastname = Column(String)                           # строка
    age = Column(Integer)                               # целое число
    slug = Column(String, unique=True, index=True)      # строка, уникальная, с индексом.
    # объект связи с таблицей Task, где back_populates='user'.
    tasks = relationship('Task', back_populates='user')


from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))
