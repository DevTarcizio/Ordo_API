from http import HTTPStatus


def test_token_route(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_token_route_error_email(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.username, 'password': user.password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect Email'}


def test_token_route_error_password(client, user):
    response = client.post(
        '/auth/token/', data={'username': user.email, 'password': user.password}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect Password'}
