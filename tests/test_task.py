def test_create_task(client, token):
    response = client.post(
        '/task/create',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'task test', 'description': 'desc test', 'state': 'todo'},
    )

    assert response.json() == {
        'id': 1,
        'title': 'task test',
        'description': 'desc test',
        'state': 'todo',
    }
