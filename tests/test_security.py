from http import HTTPStatus

from jwt import decode

from ordo_fast.security import ALGORITHM, SECRET_KEY, create_access_token


def test_access_create_token():
    data = {'teste': 'testado'}
    token = create_access_token(data)

    decoded_token = decode(token, SECRET_KEY, algorithms=ALGORITHM)
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
