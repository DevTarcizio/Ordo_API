from http import HTTPStatus

from ordo_fast.schemas import UserPublic


def test_create_user(client):

    response = client.post(
        '/users/register',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
            'role': 'player',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'role': 'player',
        'id': 1,
    }


def test_create_user_error_username(client, user_defined):
    response = client.post(
        '/users/register',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
            'role': 'player',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_error_email(client, user_defined):
    response = client.post(
        '/users/register',
        json={
            'username': 'bob',
            'email': 'alice@example.com',
            'password': 'secret',
            'role': 'player',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump(mode='json')
    response = client.get('/users/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_unique_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump(mode='json')
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_unique_user_error(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ID not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
            'role': 'player',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'role': 'player',
        'id': 1,
    }


def test_user_trying_update_another_user_error(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
            'role': 'player',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_update_user_integrity_error(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': other_user.email,
            'password': other_user.password,
            'role': other_user.role.value,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'role': user.role.value,
        'id': user.id,
    }


def test_delete_user_error(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
