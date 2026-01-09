from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ordo_fast.database import get_session
from ordo_fast.models import User
from ordo_fast.schemas import Message, Token, UserList, UserPublic, UserSchema
from ordo_fast.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI(title='Ordo Praesidium')


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
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
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
    current_user: User = Depends(get_current_user),
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
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
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
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return current_user


@app.post('/token/', response_model=Token)
def login_for_acess_token(
    # Depends vazio para garantir que irá ter o form data
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):

    # Buscamos um usuário no banco com o mesmo email do form, caso exista um email
    # passamos para verificar senha, caso não, retornamos um erro,
    user_db = session.scalar(select(User).where(User.email == form_data.username))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Incorrect Email'
        )

    # Verificação da senha
    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Incorrect Password'
        )

    access_token = create_access_token(data={'sub': user_db.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}
