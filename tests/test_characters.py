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
