from pydantic import BaseModel


class BaseUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CreateUser(BaseUser):
    username: str


class UpdateUser(BaseUser):
    pass


class BaseTask(BaseModel):
    title: str
    content: str
    priority: int


class CreateTask(BaseTask):
    pass


class UpdateTask(BaseTask):
    pass
