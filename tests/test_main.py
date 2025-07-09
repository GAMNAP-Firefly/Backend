import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Тест корневого эндпоинта."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


def test_health_check():
    """Тест эндпоинта проверки здоровья."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "debug" in data


def test_docs_endpoint():
    """Тест доступности документации."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Тест доступности ReDoc документации."""
    response = client.get("/redoc")
    assert response.status_code == 200 