from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ordo_fast.database import get_session
from ordo_fast.models import User
from ordo_fast.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(title='Ordo Praesidium')
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'olá mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    # Verifica se no banco existe um username ou email igual ao enviado para
    # o post
    db_user = session.scalar(
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
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,  # Define a quantidade máxima de registro por página
    offset: int = 0,  # Define quantos registros vai pular
    session: Session = Depends(get_session),  # Recebemos a session com o db
):

    # Realizamos a busca no db e retornamos, como temos o modelo de resposta
    # Userlist, vai retornar tudo em formato de lista, já formatado
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):

    # realizamos a busca no db pelo usuário dado a função
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='ID not found'
        )

    return user_db


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    # buscamos o usuário que queremos editar no db
    user_db = session.scalar(select(User).where(User.id == user_id))

    # lança uma exceção se o usuário não existir
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='ID not found'
        )

    try:
        # realiza a edição do usuário
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        # como o usuário já existe, nao fazemos um add, apenas o commit
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int, session: Session = Depends(get_session)):

    # buscamos o usuário que será apagado, verificamos se o ID existe, e então
    # apagamos o usuário
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='ID not found'
        )

    session.delete(user_db)
    session.commit()

    return user_db
