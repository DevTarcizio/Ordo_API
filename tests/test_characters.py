from http import HTTPStatus

import pytest

from ordo_fast.models import Character

from .factories import CharacterFactory


def test_create_character(client, token, user):
    payload = CharacterFactory.build(user_id=user.id)

    response = client.post(
        '/characters/create',
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert 'id' in data
    assert data['name'] == payload['name']


@pytest.mark.asyncio
async def test_read_characters_for_user_logged(client, token, user, session):
    expected_characters = 3
    payload = CharacterFactory.build_batch(expected_characters)

    characters = [Character(**p, user_id=user.id) for p in payload]

    session.add_all(characters)
    await session.commit()

    response = client.get(
        '/characters/list', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['characters']) == expected_characters


def test_read_character_per_id(client, token, user, character):
    response = client.get(
        f'/characters/{character.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['name'] == character.name


def test_read_character_error_id(client, token, user, character):
    response = client.get(
        '/characters/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Character not found'}


def test_read_character_from_another_user_error(
    client, user, token, other_user, other_token
):
    payload = CharacterFactory.build(user_id=user.id)

    response = client.post(
        '/characters/create',
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    character = response.json()
    character_id = character['id']

    response = client.get(
        f'/characters/{character_id}',
        headers={'Authorization': f'Bearer {other_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'This is not your character'}


def test_update_character_via_patch(client, token, user, character):
    response = client.patch(
        f'/characters/{character.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Brock Grant'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'Brock Grant'


def test_update_character_via_patch_error_id(client, token, user, character):
    response = client.patch(
        '/characters/2',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Brock Grant'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Character not found'}


def test_update_character_via_patch_from_another_user(
    client, other_token, character
):
    response = client.patch(
        f'/characters/{character.id}',
        headers={'Authorization': f'Bearer {other_token}'},
        json={'name': 'Brock Grant'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'This is not your character'}


def test_delete_character(client, user, session, character, token):
    response = client.delete(
        f'/characters/{character.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == f'Character: {character.name} deleted'


def test_delete_character_error_id(client, token, user, character):
    response = client.delete(
        '/characters/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Character not found'}


def test_delete_character_from_another_user_error(client, other_token, character):
    response = client.delete(
        f'/characters/{character.id}',
        headers={'Authorization': f'Bearer {other_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'This is not your character'}
