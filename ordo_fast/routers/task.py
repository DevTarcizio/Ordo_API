from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ordo_fast.database import get_session
from ordo_fast.models import User
from ordo_fast.security import get_current_user

router = APIRouter(prefix='/task', tags=['task'])

DBsession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


@router.post('/create')
async def create_task(session: DBsession, user: Current_user):
    return {'Criado?': 'Sim', 'User_id': user.id}


@router.get('/list')
async def list_tasks():
    return {'Tarefa': 'Corrigir Terminal'}
