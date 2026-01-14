from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from ordo_fast.models import TaskState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    limit: int = 10  # Define a quantidade máxima de registro por página
    offset: int = 0  # Define quantos registros vai pular


class FilterTask(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None


class TaskSchema(BaseModel):
    title: str
    description: str
    state: TaskState


class TaskPublic(TaskSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
