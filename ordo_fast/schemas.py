from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr

from ordo_fast.enums import Classes, Origins, Ranks
from ordo_fast.models import UserRoles


class BaseSchema(BaseModel):
    model_config = {'json_encoders': {Enum: lambda v: v.value}}


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRoles


class UserPublic(BaseSchema):
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


class CharacterUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    origin: Origins | None = None
    character_class: Classes | None = None
    rank: Ranks | None = None
    nex_total: int | None = None
    nex_class: int | None = None
    nex_subclass: int | None = None
    healthy_points: int | None = None
    sanity_points: int | None = None
    effort_points: int | None = None
    atrib_agility: int | None = None
    atrib_intellect: int | None = None
    atrib_vitallity: int | None = None
    atrib_presence: int | None = None
    atrib_strength: int | None = None


class CharacterPublic(BaseModel):
    name: str
    id: int
    user_id: int


class CharacterList(BaseModel):
    characters: list[CharacterSchema]
