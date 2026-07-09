import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.main import app
from src.database.session import get_db


def override_get_db():
    db = MagicMock()
    yield db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200
