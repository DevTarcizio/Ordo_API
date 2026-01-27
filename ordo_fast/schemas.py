from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator

from ordo_fast.enums import Classes, Origins, Ranks, Subclasses, Trails
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


class CharacterCreate(BaseModel):
    name: str
    age: int
    origin: Origins
    character_class: Classes
    rank: Ranks
    trail: Trails
    subclass: Subclasses
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

    @model_validator(mode='after')
    def check_subclass_and_trail(self):
        character_class = self.character_class
        subclass = self.subclass
        trail = self.trail

        if subclass.value == character_class.value:
            raise ValueError('Subclasse nao pode ser igual a classe')

        allowed_trails = CLASS_TRAIL_MAP.get(character_class, [])
        if trail not in allowed_trails:
            raise ValueError(
                f'{trail} não é permitida com a classe: {character_class}'
            )

        return self


class CharacterRead(CharacterCreate):
    id: int
    user_id: int


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


class CharacterList(BaseModel):
    characters: list[CharacterRead]


CLASS_TRAIL_MAP = {
    Classes.mundano: [Trails.none],
    Classes.transformado: [Trails.none],
    Classes.combatente: [
        Trails.aniquilador,
        Trails.comandante_de_campo,
        Trails.guerreiro,
        Trails.operacoes_especiais,
        Trails.tropa_de_choque,
    ],
    Classes.especialista: [
        Trails.atirador_de_elite,
        Trails.infiltrador,
        Trails.medico_de_campo,
        Trails.negociador,
        Trails.tecnico,
    ],
    Classes.ocultista: [
        Trails.conduite,
        Trails.flagelador,
        Trails.graduado,
        Trails.intuitivo,
        Trails.lamina_paranormal,
    ],
}
