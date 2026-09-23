from types import SimpleNamespace
import pytest

from app.api.dependencies import get_current_user
from app.main import app

# UUIDs válidos para os testes
USER_UUID = "22222222-2222-2222-2222-222222222222"
STARTUP_UUID = "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def mock_authenticated_user():
    """Sobrescreve a dependência get_current_user para simular um usuário autenticado."""
    fake_user = SimpleNamespace(id=USER_UUID, email="logged_user@example.com")
    app.dependency_overrides[get_current_user] = lambda: fake_user
    yield fake_user
    app.dependency_overrides.clear()


@pytest.fixture
def mock_startup_data():
    """Fixture com um objeto de startup padrão retornado do banco."""
    return {
        "id": STARTUP_UUID,
        "user_id": USER_UUID,
        "name": "TechVentures",
        "image_url": "https://example.com/startup.png",
        "description": "Plataforma SaaS para gestão de startups",
        "problem": "Falta de visibilidade centralizada",
        "solution": "Dashboard em tempo real",
        "segment": "B2B SaaS",
        "target_location": "Brasil",
        "stage": "mvp",
        "primary_revenue_model": "saas",
        "revenue_model_details": "Mensalidade R$ 199/mês",
        "status": "active",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }


# --- 1. Testes de Criação (POST /startups) ---

def test_create_startup_success(client, monkeypatch, mock_authenticated_user, mock_startup_data):
    async def fake_create_startup(user_id, payload):
        return mock_startup_data

    monkeypatch.setattr("app.api.startup.startup_service.create_startup", fake_create_startup)

    payload = {
        "name": "TechVentures",
        "image_url": "https://example.com/startup.png",
        "description": "Plataforma SaaS para gestão de startups",
        "problem": "Falta de visibilidade centralizada",
        "solution": "Dashboard em tempo real",
        "segment": "B2B SaaS",
        "target_location": "Brasil",
        "stage": "mvp",
        "primary_revenue_model": "saas",
        "revenue_model_details": "Mensalidade R$ 199/mês",
    }

    response = client.post("/startups", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == STARTUP_UUID
    assert body["user_id"] == USER_UUID
    assert body["name"] == "TechVentures"
    assert body["image_url"] == "https://example.com/startup.png"
    assert body["stage"] == "mvp"


# --- 2. Testes de Listagem (GET /startups) ---

def test_get_my_startups_success(client, monkeypatch, mock_authenticated_user, mock_startup_data):
    async def fake_get_user_startups(user_id):
        return [mock_startup_data]

    monkeypatch.setattr("app.api.startup.startup_service.get_user_startups", fake_get_user_startups)

    response = client.get("/startups")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["name"] == "TechVentures"
    assert body[0]["image_url"] == "https://example.com/startup.png"


# --- 3. Testes de Busca por ID (GET /startups/{id}) ---

def test_get_startup_by_id_success(client, monkeypatch, mock_authenticated_user, mock_startup_data):
    async def fake_get_startup_by_id(startup_id, user_id):
        return mock_startup_data

    monkeypatch.setattr("app.api.startup.startup_service.get_startup_by_id", fake_get_startup_by_id)

    response = client.get(f"/startups/{STARTUP_UUID}")

    assert response.status_code == 200
    assert response.json()["id"] == STARTUP_UUID
    assert response.json()["image_url"] == "https://example.com/startup.png"


def test_get_startup_by_id_not_found(client, monkeypatch, mock_authenticated_user):
    async def fake_get_startup_by_id(startup_id, user_id):
        return None

    monkeypatch.setattr("app.api.startup.startup_service.get_startup_by_id", fake_get_startup_by_id)

    response = client.get("/startups/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["detail"] == "Startup não encontrada."


# --- 4. Testes de Atualização (PATCH /startups/{id}) ---

def test_update_startup_success(client, monkeypatch, mock_authenticated_user, mock_startup_data):
    updated_data = {
        **mock_startup_data,
        "name": "TechVentures V2",
        "image_url": "https://example.com/startup-v2.png",
        "stage": "launched",
    }

    async def fake_update_startup(startup_id, user_id, payload):
        return updated_data

    monkeypatch.setattr("app.api.startup.startup_service.update_startup", fake_update_startup)

    response = client.patch(
        f"/startups/{STARTUP_UUID}",
        json={
            "name": "TechVentures V2",
            "image_url": "https://example.com/startup-v2.png",
            "stage": "launched",
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "TechVentures V2"
    assert body["image_url"] == "https://example.com/startup-v2.png"
    assert body["stage"] == "launched"


def test_update_startup_not_found(client, monkeypatch, mock_authenticated_user):
    async def fake_update_startup(startup_id, user_id, payload):
        return None

    monkeypatch.setattr("app.api.startup.startup_service.update_startup", fake_update_startup)

    response = client.patch(
        "/startups/00000000-0000-0000-0000-000000000000",
        json={"name": "Nome Inexistente"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Startup não encontrada."


# --- 5. Testes de Exclusão (DELETE /startups/{id}) ---

def test_delete_startup_success(client, monkeypatch, mock_authenticated_user):
    async def fake_delete_startup(startup_id, user_id):
        return True

    monkeypatch.setattr("app.api.startup.startup_service.delete_startup", fake_delete_startup)

    response = client.delete(f"/startups/{STARTUP_UUID}")

    assert response.status_code == 204


def test_delete_startup_not_found(client, monkeypatch, mock_authenticated_user):
    async def fake_delete_startup(startup_id, user_id):
        return False

    monkeypatch.setattr("app.api.startup.startup_service.delete_startup", fake_delete_startup)

    response = client.delete("/startups/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["detail"] == "Startup não encontrada."