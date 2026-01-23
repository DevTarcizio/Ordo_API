from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from ordo_fast.enums import Classes, Origins, Ranks
from ordo_fast.models import TaskState, UserRoles


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRoles


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    role: UserRoles
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


class CharacterSchema(BaseModel):
    name: str
    age: int
    origin: Origins
    character_class: Classes
    rank: Ranks
    nex_total: int
    nex_class: int
    nex_subclass: int
    healthy_points: int
    sanity_points: int
    effort_points: int
    atrib_agility: int
    atrib_intellect: int
    atrib_vitallity: int
    atrib_presence: int
    atrib_strength: int


class CharacterPublic(BaseModel):
    name: str
    id: int
    user_id: int


class CharacterList(BaseModel):
    characters: list[CharacterPublic]
