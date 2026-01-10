from http import HTTPStatus


def test_read_root_retorna_ok_e_ola_mundo(client):

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'olá mundo'}
