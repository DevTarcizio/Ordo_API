from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ordo_fast.database import get_session
from ordo_fast.models import Task, User
from ordo_fast.schemas import (
    FilterTask,
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
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


@router.get('/list', response_model=TaskList)
async def list_tasks(
    session: DBsession,
    user: Current_user,
    task_filter: Annotated[FilterTask, Query()],
):
    query = select(Task).where(Task.user_id == user.id)

    if task_filter.title:
        query = query.filter(Task.title.contains(task_filter.title))

    if task_filter.description:
        query = query.filter(Task.description.contains(task_filter.description))

    if task_filter.state:
        query = query.filter(Task.state == task_filter.state)

    tasks = await session.scalars(
        query.offset(task_filter.offset).limit(task_filter.limit)
    )

    return {'tasks': tasks}


@router.delete('/{task_id}')
async def delete_task(session: DBsession, user: Current_user, task_id: int):
    task = await session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    await session.delete(task)
    await session.commit()

    return {'message': 'Task has been deleted'}


@router.patch('/{task_id}', response_model=TaskPublic)
async def update_task_via_patch(
    task_id: int, session: DBsession, user: Current_user, task: TaskUpdate
):
    task_db = await session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(task_db, key, value)

    await session.commit()
    await session.refresh(task_db)

    return task_db
