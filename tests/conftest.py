import pytest
from fastapi.testclient import TestClient

from ordo_fast.app import app


@pytest.fixture
def client():
    return TestClient(app)
