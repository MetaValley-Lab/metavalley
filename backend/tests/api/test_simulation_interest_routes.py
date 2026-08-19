from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


USER_UUID = "22222222-2222-2222-2222-222222222222"
STARTUP_UUID = "11111111-1111-1111-1111-111111111111"
INTEREST_UUID = "33333333-3333-3333-3333-333333333333"


@pytest.fixture
def mock_authenticated_user():
    """Simula um usuário autenticado."""
    fake_user = SimpleNamespace(
        id=USER_UUID,
        email="founder@example.com"
    )

    app.dependency_overrides[get_current_user] = lambda: fake_user

    yield fake_user

    app.dependency_overrides.clear()


@pytest.fixture
def mock_interest_data():
    """Registro padrão de interesse retornado pelo service."""
    return {
        "id": INTEREST_UUID,
        "user_id": USER_UUID,
        "startup_id": STARTUP_UUID,
        "email": "founder@example.com",
        "created_at": "2026-01-01T00:00:00Z",
    }


def test_create_simulation_interest(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_interest_data
):
    """
    Founder entra na lista de espera da simulação.
    """

    async def fake_create_interest(user_id, email, payload):
        assert user_id == USER_UUID
        assert email == "founder@example.com"
        assert str(payload.startup_id) == STARTUP_UUID

        return mock_interest_data

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.create_interest",
        fake_create_interest
    )

    payload = {
        "startup_id": STARTUP_UUID
    }

    response = client.post(
        "/simulation-interests",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == INTEREST_UUID
    assert data["user_id"] == USER_UUID
    assert data["startup_id"] == STARTUP_UUID
    assert data["email"] == "founder@example.com"


def test_create_simulation_interest_does_not_accept_user_data(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_interest_data
):
    """
    user_id e email não devem ser fornecidos pelo frontend.
    """

    async def fake_create_interest(user_id, email, payload):
        assert user_id == USER_UUID
        assert email == "founder@example.com"

        return mock_interest_data

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.create_interest",
        fake_create_interest
    )

    payload = {
        "startup_id": STARTUP_UUID,
        "user_id": "99999999-9999-9999-9999-999999999999",
        "email": "outro@example.com",
    }

    response = client.post(
        "/simulation-interests",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    # Os dados retornados devem representar o usuário autenticado.
    assert data["user_id"] == USER_UUID
    assert data["email"] == "founder@example.com"


def test_create_simulation_interest_error(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Não deve permitir registrar interesse quando o service
    rejeita a operação.
    """

    async def fake_create_interest(user_id, email, payload):
        raise Exception(
            "Startup não encontrada ou você não tem permissão."
        )

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.create_interest",
        fake_create_interest
    )

    payload = {
        "startup_id": STARTUP_UUID
    }

    response = client.post(
        "/simulation-interests",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Startup não encontrada ou você não tem permissão."
    )


def test_create_duplicate_simulation_interest(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Não permite que o founder entre duas vezes na lista
    da mesma startup.
    """

    async def fake_create_interest(user_id, email, payload):
        raise Exception(
            "Você já demonstrou interesse nesta simulação."
        )

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.create_interest",
        fake_create_interest
    )

    payload = {
        "startup_id": STARTUP_UUID
    }

    response = client.post(
        "/simulation-interests",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Você já demonstrou interesse nesta simulação."
    )


def test_get_my_simulation_interest_true(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Verifica que o founder já está na lista de espera.
    """

    async def fake_has_user_interest(user_id, startup_id):
        assert user_id == USER_UUID
        assert startup_id == STARTUP_UUID

        return True

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.has_user_interest",
        fake_has_user_interest
    )

    response = client.get(
        f"/simulation-interests/startup/{STARTUP_UUID}/me"
    )

    assert response.status_code == 200
    assert response.json() == {
        "interested": True
    }


def test_get_my_simulation_interest_false(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Verifica que o founder ainda não está na lista.
    """

    async def fake_has_user_interest(user_id, startup_id):
        assert user_id == USER_UUID
        assert startup_id == STARTUP_UUID

        return False

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.has_user_interest",
        fake_has_user_interest
    )

    response = client.get(
        f"/simulation-interests/startup/{STARTUP_UUID}/me"
    )

    assert response.status_code == 200
    assert response.json() == {
        "interested": False
    }


def test_delete_simulation_interest(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Founder remove seu interesse da lista de espera.
    """

    async def fake_delete_interest(interest_id, user_id):
        assert interest_id == INTEREST_UUID
        assert user_id == USER_UUID

        return True

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.delete_interest",
        fake_delete_interest
    )

    response = client.delete(
        f"/simulation-interests/{INTEREST_UUID}"
    )

    assert response.status_code == 204


def test_delete_simulation_interest_not_found(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Não permite remover um interesse inexistente ou
    que não pertença ao usuário autenticado.
    """

    async def fake_delete_interest(interest_id, user_id):
        return False

    monkeypatch.setattr(
        "app.api.simulation_interest.simulation_interest_service.delete_interest",
        fake_delete_interest
    )

    response = client.delete(
        f"/simulation-interests/{INTEREST_UUID}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Interesse não encontrado ou acesso negado."
    )


def test_create_simulation_interest_requires_startup_id(
    client: TestClient,
    mock_authenticated_user
):
    """
    startup_id é obrigatório para registrar o interesse.
    """

    response = client.post(
        "/simulation-interests",
        json={}
    )

    assert response.status_code == 422
    
