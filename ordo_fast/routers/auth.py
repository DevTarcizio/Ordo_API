from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from ordo_fast.database import get_session
from ordo_fast.models import User
from ordo_fast.schemas import Token
from ordo_fast.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['Auth'])
DBsession = Annotated[Session, Depends(get_session)]
Auth2_request_form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token/', response_model=Token)
def login_for_acess_token(
    # Depends vazio para garantir que irá ter o form data
    session: DBsession,
    form_data: Auth2_request_form,
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
