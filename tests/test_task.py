from http import HTTPStatus

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from ordo_fast.models import Task

from .factories import TaskFactory


def test_create_task(client, token, mock_db_time):

    with mock_db_time(model=Task) as time:
        response = client.post(
            '/task/create',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': 'task test',
                'description': 'desc test',
                'state': 'todo',
            },
        )

    assert response.json() == {
        'id': 1,
        'title': 'task test',
        'description': 'desc test',
        'state': 'todo',
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
    }

@pytest.mark.asyncio
async def test_list_tasks_validate_values(
    session, token, user, mock_db_time, client
):

    with mock_db_time(model=Task) as time:
        task = TaskFactory(user_id=user.id)
        session.add(task)
        await session.commit()

    await session.refresh(task)

    response = client.get(
        '/task/list', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json()['tasks'] == [
        {
            'title': task.title,
            'description': task.description,
            'state': task.state.value,
            'id': task.id,
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        }
    ]


@pytest.mark.asyncio
async def test_list_tasks_should_return_5_tasks(
    session: Session, client, user, token
):
    expected_tasks = 5
    session.add_all(TaskFactory.create_batch(expected_tasks, user_id=user.id))
    await session.commit()  # type: ignore

    response = client.get(
        '/task/list', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_list_tasks_pagination_should_return_only_2_tasks(
    session: Session, client, user, token
):
    expected_tasks = 2
    session.add_all(TaskFactory.create_batch(5, user_id=user.id))
    await session.commit()  # type: ignore

    response = client.get(
        '/task/list?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_list_tasks_filter_title(session: Session, client, user, token):
    expected_tasks = 5
    session.add_all(
        TaskFactory.create_batch(
            expected_tasks, user_id=user.id, title='test task 1'
        )
    )
    await session.commit()  # type: ignore

    response = client.get(
        '/task/list?title=test task 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_list_tasks_filter_description(
    session: Session, client, user, token
):
    expected_tasks = 5
    session.add_all(
        TaskFactory.create_batch(
            expected_tasks, user_id=user.id, description='test description'
        )
    )
    await session.commit()  # type: ignore

    response = client.get(
        '/task/list?description=test description',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_list_tasks_filter_state(session: Session, client, user, token):
    expected_tasks = 5
    session.add_all(
        TaskFactory.create_batch(expected_tasks, user_id=user.id, state='doing')
    )
    await session.commit()  # type: ignore

    response = client.get(
        '/task/list?state=doing',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_delete_task(session: Session, client, user, token):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    await session.commit()  # type: ignore

    response = client.delete(
        f'/task/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted'}


def test_delete_task_error(client, token):
    response = client.delete(
        '/task/999', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_update_task_via_patch(client, user, token, session: Session):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    await session.commit()  # type: ignore

    response = client.patch(
        f'/task/{task.id}',
        json={'title': 'teste'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste'


def test_update_task_via_patch_error(client, token):
    response = client.patch(
        '/task/999', json={}, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
