from http import HTTPStatus

from fastapi.testclient import TestClient

from ordo_fast.app import app


def test_read_root_retorna_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'olá mundo'}
