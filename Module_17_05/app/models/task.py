from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)  # целое число, первичный ключ, с индексом
    title = Column(String)                              # строка
    content = Column(String)                            # строка
    priority = Column(Integer, default=0)               # целое число, по умолчанию 0
    completed = Column(Boolean, default=False)          # булевое значение, по умолчанию False
    # целое число, внешний ключ на id из таблицы 'users', не NULL, с индексом.
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)      # строка, уникальная, с индексом.
    # объект связи с таблицей User, где back_populates = 'tasks'
    user = relationship('User', back_populates='tasks')


from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
