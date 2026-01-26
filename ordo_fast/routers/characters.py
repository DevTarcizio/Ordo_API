from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ordo_fast.database import get_session
from ordo_fast.enums import UserRoles
from ordo_fast.models import Character, User
from ordo_fast.schemas import (
    CharacterList,
    CharacterPublic,
    CharacterSchema,
    CharacterUpdate,
)
from ordo_fast.security import get_current_user

router = APIRouter(prefix='/characters', tags=['Characters'])
DBsession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


@router.post(
    '/create/', response_model=CharacterPublic, status_code=HTTPStatus.CREATED
)
async def create_character(
    character: CharacterSchema, user: Current_user, session: DBsession
):
    db_character = Character(
        name=character.name,
        age=character.age,
        origin=character.origin,
        character_class=character.character_class,
        rank=character.rank,
        user_id=user.id,
        nex_total=character.nex_total,
        nex_class=character.nex_class,
        nex_subclass=character.nex_subclass,
        healthy_points=character.healthy_points,
        sanity_points=character.sanity_points,
        effort_points=character.effort_points,
        atrib_agility=character.atrib_agility,
        atrib_intellect=character.atrib_intellect,
        atrib_vitallity=character.atrib_vitallity,
        atrib_presence=character.atrib_presence,
        atrib_strength=character.atrib_strength,
    )

    session.add(db_character)
    await session.commit()
    await session.refresh(db_character)

    return db_character


@router.get('/list', response_model=CharacterList, status_code=HTTPStatus.OK)
async def read_characters_for_user_logged(user: Current_user, session: DBsession):
    db_characters = await session.scalars(
        select(Character).where(Character.user_id == user.id)
    )

    return {'characters': db_characters}


@router.get(
    '/{character_id}/', response_model=CharacterSchema, status_code=HTTPStatus.OK
)
async def read_character(
    user: Current_user, session: DBsession, character_id: int
):
    db_character = await session.scalar(
        select(Character).where(Character.id == character_id)
    )

    if not db_character:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Character not found'
        )

    if db_character.user_id != user.id and user.role != UserRoles.master:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='This is not your character'
        )

    return db_character


@router.patch(
    '/{character_id}/', response_model=CharacterSchema, status_code=HTTPStatus.OK
)
async def update_character_info_via_patch(
    character_id: int,
    user: Current_user,
    session: DBsession,
    character: CharacterUpdate,
):
    db_character = await session.scalar(
        select(Character).where(Character.id == character_id)
    )

    if not db_character:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Character not found'
        )

    if db_character.user_id != user.id and user.role != UserRoles.master:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='This is not your character'
        )

    for key, value in character.model_dump(exclude_unset=True).items():
        setattr(db_character, key, value)

    await session.commit()
    await session.refresh(db_character)

    return db_character


@router.delete('/{character_id}/', status_code=HTTPStatus.OK)
async def delete_character(
    character_id: int, user: Current_user, session: DBsession
):
    db_character = await session.scalar(
        select(Character).where(Character.id == character_id)
    )

    if not db_character:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Character not found'
        )

    if db_character.user_id != user.id and user.role != UserRoles.master:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='This is not your character'
        )

    await session.delete(db_character)
    await session.commit()

    return f'Character: {db_character.name} deleted'
