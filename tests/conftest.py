from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from ordo_fast.app import app
from ordo_fast.database import get_session
from ordo_fast.models import User, table_registry


@pytest.fixture
def client(session: Session):
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


@pytest.fixture
def session():

    # Criamos o banco em memória, desligamos a verificação de mesma thread para os
    # testes

    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # Cria todas as tabelas para realizar teste
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Apaga todas as tabelas para realizar teste
    table_registry.metadata.drop_all(engine)


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


@pytest.fixture
def user(session: Session):
    user_test = User(
        username='alice', email='alice@example.com', password='secret'
    )
    session.add(user_test)
    session.commit()
    session.refresh(user_test)

    return user_test
