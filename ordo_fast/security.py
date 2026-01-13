from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ordo_fast.database import get_session
from ordo_fast.models import User
from ordo_fast.settings import Settings

# constantes para a criação do token

# Configuração padrão do pwd
pwd_context = PasswordHash.recommended()

# ler o token jwt enviado no header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


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
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES  # type: ignore
    )
    to_encode.update({'exp': expire})

    # Fazemos o encode do token, e o retornamos
    encoded_jwt = encode(
        to_encode,
        Settings().SECRET_KEY,  # type: ignore
        algorithm=Settings().ALGORITHM,  # type: ignore
    )
    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token,
            Settings().SECRET_KEY,  # type: ignore
            algorithms=Settings().ALGORITHM,  # type: ignore
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = await session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user
