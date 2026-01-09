from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from ordo_fast.database import get_session
from ordo_fast.models import User

# constantes para a criação do token
SECRET_KEY = 'my_secret_key'  # Isso é provisório depois trocar por um hash secret
ALGORITHM = 'HS256'  # algoritmo usado nessa codificação
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # tempo de expiração do token

# Configuração padrão do pwd
pwd_context = PasswordHash.recommended()

# ler o token jwt enviado no header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(normal_password: str, hashed_password: str):
    return pwd_context.verify(normal_password, hashed_password)


# A função recebe os dados em formato de dicionário
def create_access_token(data: dict):

    # Criamos uma cópia dos dados
    to_encode = data.copy()

    # Fazemos o calculo com a time zone UTC para o tempo de expiração ser de
    # 30 minutos e então adicionamos essa claim
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    # Fazemos o encode do token, e o retornamos
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user
