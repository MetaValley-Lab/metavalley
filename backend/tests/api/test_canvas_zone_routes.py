from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


USER_UUID = "22222222-2222-2222-2222-222222222222"
STARTUP_UUID = "11111111-1111-1111-1111-111111111111"
CANVAS_ZONE_UUID = "33333333-3333-3333-3333-333333333333"


@pytest.fixture
def mock_authenticated_user():
    """Sobrescreve a dependência get_current_user para simular um usuário autenticado."""
    fake_user = SimpleNamespace(
        id=USER_UUID,
        email="logged_user@example.com"
    )

    app.dependency_overrides[get_current_user] = lambda: fake_user

    yield fake_user

    app.dependency_overrides.clear()


@pytest.fixture
def mock_canvas_zone_data():
    """Fixture com uma Canvas Zone padrão retornada pelo banco."""
    return {
        "id": CANVAS_ZONE_UUID,
        "startup_id": STARTUP_UUID,
        "zone_key": "value_proposition",
        "content": "Ajudamos startups a validar seus produtos.",
        "status": "filled",
        "filled_by": "founder",
        "updated_at": "2026-01-01T00:00:00Z",
        "previous_content": None,
    }


def test_create_canvas_zone_default_values(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_canvas_zone_data
):
    """
    Testa a criação de uma Canvas Zone sem informar
    status e filled_by.

    O sistema deve assumir:
    - status = to_define
    - filled_by = founder
    """

    async def fake_create_zone(user_id, payload):
        assert str(payload.startup_id) == STARTUP_UUID
        assert payload.zone_key.value == "value_proposition"
        assert payload.status.value == "to_define"
        assert payload.filled_by.value == "founder"

        return {
            **mock_canvas_zone_data,
            "status": "to_define",
            "content": None,
            "filled_by": "founder",
        }

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.create_zone",
        fake_create_zone
    )

    payload = {
        "startup_id": STARTUP_UUID,
        "zone_key": "value_proposition"
    }

    response = client.post(
        "/canvas-zones",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == CANVAS_ZONE_UUID
    assert data["startup_id"] == STARTUP_UUID
    assert data["zone_key"] == "value_proposition"
    assert data["content"] is None
    assert data["status"] == "to_define"
    assert data["filled_by"] == "founder"
    assert data["previous_content"] is None


def test_create_canvas_zone_with_agent(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_canvas_zone_data
):
    """
    Testa a criação de uma Canvas Zone informando
    explicitamente um agente como responsável.
    """

    async def fake_create_zone(user_id, payload):
        assert payload.filled_by.value == "ceo"
        assert payload.status.value == "in_progress"

        return {
            **mock_canvas_zone_data,
            "status": "in_progress",
            "filled_by": "ceo",
            "content": "Ajudamos startups a validar seus produtos."
        }

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.create_zone",
        fake_create_zone
    )

    payload = {
        "startup_id": STARTUP_UUID,
        "zone_key": "value_proposition",
        "content": "Ajudamos startups a validar seus produtos.",
        "status": "in_progress",
        "filled_by": "ceo"
    }

    response = client.post(
        "/canvas-zones",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["content"] == "Ajudamos startups a validar seus produtos."
    assert data["status"] == "in_progress"
    assert data["filled_by"] == "ceo"


def test_get_canvas_zones_by_startup(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_canvas_zone_data
):
    """
    Testa a listagem das Canvas Zones de uma startup.
    """

    async def fake_get_zones(startup_id, user_id):
        assert startup_id == STARTUP_UUID
        assert user_id == USER_UUID

        return [mock_canvas_zone_data]

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.get_zones_by_startup",
        fake_get_zones
    )

    response = client.get(
        f"/canvas-zones/startup/{STARTUP_UUID}"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == CANVAS_ZONE_UUID
    assert data[0]["startup_id"] == STARTUP_UUID
    assert data[0]["zone_key"] == "value_proposition"
    assert data[0]["status"] == "filled"
    assert data[0]["filled_by"] == "founder"


def test_get_canvas_zone_by_id(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_canvas_zone_data
):
    """
    Testa a consulta de uma Canvas Zone específica.
    """

    async def fake_get_zone(zone_id, user_id):
        assert zone_id == CANVAS_ZONE_UUID
        assert user_id == USER_UUID

        return mock_canvas_zone_data

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.get_zone_by_id",
        fake_get_zone
    )

    response = client.get(
        f"/canvas-zones/{CANVAS_ZONE_UUID}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == CANVAS_ZONE_UUID
    assert data["startup_id"] == STARTUP_UUID
    assert data["zone_key"] == "value_proposition"
    assert data["content"] == "Ajudamos startups a validar seus produtos."


def test_get_canvas_zone_not_found(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Testa o retorno 404 quando a Canvas Zone não existe
    ou não pertence ao usuário.
    """

    async def fake_get_zone(zone_id, user_id):
        return None

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.get_zone_by_id",
        fake_get_zone
    )

    response = client.get(
        f"/canvas-zones/{CANVAS_ZONE_UUID}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Canvas Zone não encontrada ou acesso negado."
    )


def test_update_canvas_zone_content(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_canvas_zone_data
):
    """
    Testa a atualização do conteúdo de uma Canvas Zone.
    """

    updated_data = {
        **mock_canvas_zone_data,
        "content": "Ajudamos founders a validar e estruturar seus negócios.",
        "previous_content": "Ajudamos startups a validar seus produtos.",
        "filled_by": "ceo",
        "status": "filled",
    }

    async def fake_update_zone(zone_id, user_id, payload):
        assert zone_id == CANVAS_ZONE_UUID
        assert user_id == USER_UUID
        assert payload.content == (
            "Ajudamos founders a validar e estruturar seus negócios."
        )
        assert payload.filled_by.value == "ceo"

        return updated_data

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.update_zone",
        fake_update_zone
    )

    payload = {
        "content": "Ajudamos founders a validar e estruturar seus negócios.",
        "filled_by": "ceo",
        "status": "filled"
    }

    response = client.patch(
        f"/canvas-zones/{CANVAS_ZONE_UUID}",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == (
        "Ajudamos founders a validar e estruturar seus negócios."
    )
    assert data["previous_content"] == (
        "Ajudamos startups a validar seus produtos."
    )
    assert data["filled_by"] == "ceo"
    assert data["status"] == "filled"


def test_update_canvas_zone_status(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_canvas_zone_data
):
    """
    Testa a atualização somente do status.
    """

    updated_data = {
        **mock_canvas_zone_data,
        "status": "in_progress",
    }

    async def fake_update_zone(zone_id, user_id, payload):
        assert payload.status.value == "in_progress"
        assert payload.content is None
        return updated_data

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.update_zone",
        fake_update_zone
    )

    payload = {
        "status": "in_progress"
    }

    response = client.patch(
        f"/canvas-zones/{CANVAS_ZONE_UUID}",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "in_progress"
    assert data["content"] == mock_canvas_zone_data["content"]


def test_update_canvas_zone_not_found(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Testa o retorno 404 quando a Canvas Zone não existe
    ou não pertence ao usuário.
    """

    async def fake_update_zone(zone_id, user_id, payload):
        return None

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.update_zone",
        fake_update_zone
    )

    payload = {
        "content": "Novo conteúdo."
    }

    response = client.patch(
        f"/canvas-zones/{CANVAS_ZONE_UUID}",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Canvas Zone não encontrada ou acesso negado."
    )


def test_delete_canvas_zone(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Testa a deleção de uma Canvas Zone.
    """

    async def fake_delete_zone(zone_id, user_id):
        assert zone_id == CANVAS_ZONE_UUID
        assert user_id == USER_UUID

        return True

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.delete_zone",
        fake_delete_zone
    )

    response = client.delete(
        f"/canvas-zones/{CANVAS_ZONE_UUID}"
    )

    assert response.status_code == 204


def test_delete_canvas_zone_not_found(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Testa a deleção de uma Canvas Zone inexistente
    ou sem permissão.
    """

    async def fake_delete_zone(zone_id, user_id):
        return False

    monkeypatch.setattr(
        "app.api.canvas_zone.canvas_zone_service.delete_zone",
        fake_delete_zone
    )

    response = client.delete(
        f"/canvas-zones/{CANVAS_ZONE_UUID}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Canvas Zone não encontrada ou acesso negado."
    )