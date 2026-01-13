from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from ordo_fast.app import app
from ordo_fast.database import get_session
from ordo_fast.models import User, table_registry
from ordo_fast.security import get_password_hash


@pytest.fixture
def client(session: AsyncSession):
    # a função get session retorna a sessão que está linkada no nosso banco real,
    # como nos testes usamos um db em memória, precisamos dessa session em memória
    # também, por isso trocamos a dependencia do get_session para get_session_test
    # assim nos testes usaremos a sessão de teste e não a real

    def get_session_test():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_test
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():

    # Criamos o banco em memória, desligamos a verificação de mesma thread para os
    # testes

    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # o with permite que tenha um commit automático no fim, e ao invés de usarmos
    # uma session, usamos uma conexão
    async with engine.begin() as conn:
        # run sync para criarmos as tabelas de forma sicrona para não
        # acontecer confusões na criação
        await conn.run_sync(table_registry.metadata.create_all)

    # criamos a session para ser usada
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    # apagamos todas as tabelas no fim do teste
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'update_at'):
            target.update_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'secret'
    user_test = User(
        username='alice',
        email='alice@example.com',
        password=get_password_hash(password),
    )
    session.add(user_test)
    await session.commit()
    await session.refresh(user_test)

    user_test.clean_password = password  # type: ignore

    return user_test


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
