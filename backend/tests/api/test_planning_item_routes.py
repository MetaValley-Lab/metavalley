from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app

USER_UUID = "22222222-2222-2222-2222-222222222222"
STARTUP_UUID = "11111111-1111-1111-1111-111111111111"
PLANNING_ITEM_UUID = "33333333-3333-3333-3333-333333333333"


@pytest.fixture
def mock_authenticated_user():
    """Sobrescreve a dependência get_current_user para simular um usuário autenticado."""
    fake_user = SimpleNamespace(id=USER_UUID, email="logged_user@example.com")
    app.dependency_overrides[get_current_user] = lambda: fake_user
    yield fake_user
    app.dependency_overrides.clear()


@pytest.fixture
def mock_planning_item_data():
    """Fixture com um objeto de item de planejamento padrão retornado do banco."""
    return {
        "id": PLANNING_ITEM_UUID,
        "startup_id": STARTUP_UUID,
        "content": "Validar MVP com 10 clientes.",
        "created_by": "founder",
        "last_updated_by": "founder",
        "completed": False,
        "completed_at": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }


def test_create_planning_item_default_founder(client: TestClient, monkeypatch, mock_authenticated_user, mock_planning_item_data):
    """
    Testa a criação de um item de planejamento SEM passar created_by.
    O sistema deve assumir que foi o 'founder'.
    """
    async def fake_create_item(user_id, payload):
        return mock_planning_item_data

    # Apontando para 'planning_service' dentro do módulo do router
    monkeypatch.setattr("app.api.planning_item.planning_service.create_item", fake_create_item)

    payload = {
        "startup_id": STARTUP_UUID,
        "content": "Validar MVP com 10 clientes."
    }

    response = client.post(
        "/planning-items",
        json=payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Validar MVP com 10 clientes."
    assert data["startup_id"] == STARTUP_UUID
    assert data["created_by"] == "founder"
    assert data["last_updated_by"] == "founder"
    assert data["completed"] is False


def test_get_planning_items_by_startup(client: TestClient, monkeypatch, mock_authenticated_user, mock_planning_item_data):
    """
    Testa a listagem de tarefas de uma startup.
    """
    async def fake_get_items(startup_id, user_id):
        return [mock_planning_item_data]

    monkeypatch.setattr("app.api.planning_item.planning_service.get_items_by_startup", fake_get_items)

    response = client.get(f"/planning-items/startup/{STARTUP_UUID}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["content"] == "Validar MVP com 10 clientes."


def test_delete_planning_item(client: TestClient, monkeypatch, mock_authenticated_user):
    """
    Testa a deleção de um item.
    """
    async def fake_delete_item(item_id, user_id):
        return True

    monkeypatch.setattr("app.api.planning_item.planning_service.delete_item", fake_delete_item)

    response = client.delete(f"/planning-items/{PLANNING_ITEM_UUID}")
    assert response.status_code == 204