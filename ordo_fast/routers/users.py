from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ordo_fast.database import get_session
from ordo_fast.models import User
from ordo_fast.schemas import FilterPage, UserList, UserPublic, UserSchema
from ordo_fast.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['Users'])
DBsession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
async def create_user(user: UserSchema, session: DBsession):

    # Verifica se no banco existe um username ou email igual ao enviado para
    # o post
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    # se existir algum igual, faz a verificação para ver qual é o campo que está
    # com problema e lança a exceção com o código 409 e a explicação do erro
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Username already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    # caso não haja nada igual, passa os valores que vieram do post para o db_user
    # e depois salva na session
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: DBsession,  # Recebemos a session com o db
    current_user: Current_user,
    filter_page: Annotated[FilterPage, Query()],
    # filter_page: Define quantos registros vai pular
):

    # Realizamos a busca no db e retornamos, como temos o modelo de resposta
    # Userlist, vai retornar tudo em formato de lista, já formatado
    users = await session.scalars(
        select(User).limit(filter_page.limit).offset(filter_page.offset)
    )
    return {'users': users}


@router.get('/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
async def read_user(user_id: int, session: DBsession):

    # realizamos a busca no db pelo usuário dado a função
    user_db = await session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='ID not found'
        )

    return user_db


@router.put('/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: DBsession,
    current_user: Current_user,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    try:
        # realiza a edição do usuário
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        # como o usuário já existe, nao fazemos um add, apenas o commit
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
async def delete_user(
    user_id: int,
    session: DBsession,
    current_user: Current_user,
):

    # verifica se o usuário está apagando a si mesmo
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    await session.delete(current_user)
    await session.commit()

    return current_user
