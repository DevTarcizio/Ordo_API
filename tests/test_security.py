from http import HTTPStatus

from freezegun import freeze_time
from jwt import decode

from ordo_fast.security import create_access_token
from ordo_fast.settings import Settings


def test_access_create_token():
    data = {'teste': 'testado'}
    token = create_access_token(data)

    decoded_token = decode(
        token,
        Settings().SECRET_KEY,  # type: ignore
        algorithms=Settings().ALGORITHM,  # type: ignore
    )
    assert decoded_token['teste'] == data['teste']
    assert 'exp' in decoded_token


def test_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_user_not_found(client):
    data = {'no-email': 'teste'}
    token = create_access_token(data=data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_user_not_exist_in_db(client):
    data = {'sub': 'pedro@example.com'}
    token = create_access_token(data=data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_expired_after_time(client, user):
    with freeze_time('2026-12-31 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2026-12-31 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
