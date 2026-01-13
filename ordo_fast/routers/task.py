from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ordo_fast.database import get_session
from ordo_fast.models import Task, User
from ordo_fast.schemas import TaskPublic, TaskSchema
from ordo_fast.security import get_current_user

router = APIRouter(prefix='/task', tags=['task'])

DBsession = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


@router.post('/create', response_model=TaskPublic)
async def create_task(task: TaskSchema, session: DBsession, user: Current_user):
    task_db = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=user.id,
    )

    session.add(task_db)
    await session.commit()
    await session.refresh(task_db)

    return task_db


@router.get('/list')
async def list_tasks():
    return {'Tarefa': 'Corrigir Terminal'}
