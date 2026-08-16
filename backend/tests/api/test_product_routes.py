from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from decimal import Decimal

from app.api.dependencies import get_current_user
from app.main import app


USER_UUID = "22222222-2222-2222-2222-222222222222"
STARTUP_UUID = "11111111-1111-1111-1111-111111111111"
PRODUCT_UUID = "33333333-3333-3333-3333-333333333333"


@pytest.fixture
def mock_authenticated_user():
    """Sobrescreve a dependência para simular um usuário autenticado."""
    fake_user = SimpleNamespace(
        id=USER_UUID,
        email="logged_user@example.com"
    )

    app.dependency_overrides[get_current_user] = lambda: fake_user

    yield fake_user

    app.dependency_overrides.clear()


@pytest.fixture
def mock_product_data():
    """Produto padrão retornado pelo service."""
    return {
        "id": PRODUCT_UUID,
        "startup_id": STARTUP_UUID,
        "name": "Meta Valley SaaS",
        "description": "Plataforma para gestão de startups.",
        "type": "saas",
        "price": 99.90,
        "stage": "mvp",
        "last_updated_by": "founder",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }


def test_create_product_default_founder(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_product_data
):
    """
    Testa a criação de um produto sem informar last_updated_by.
    O schema deve assumir founder como padrão.
    """

    async def fake_create_product(user_id, payload):
        return mock_product_data

    monkeypatch.setattr(
        "app.api.product.product_service.create_product",
        fake_create_product
    )

    payload = {
        "startup_id": STARTUP_UUID,
        "name": "Meta Valley SaaS",
        "description": "Plataforma para gestão de startups.",
        "type": "saas",
        "price": 99.90,
        "stage": "mvp",
    }

    response = client.post(
        "/products",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == PRODUCT_UUID
    assert data["startup_id"] == STARTUP_UUID
    assert data["name"] == "Meta Valley SaaS"
    assert data["type"] == "saas"
    assert Decimal(data["price"]) == Decimal("99.90")
    assert data["stage"] == "mvp"
    assert data["last_updated_by"] == "founder"


def test_create_product_by_cto(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_product_data
):
    """
    Testa a criação de um produto através do fluxo do CTO.
    """

    cto_product = {
        **mock_product_data,
        "last_updated_by": "cto"
    }

    async def fake_create_product(user_id, payload):
        return cto_product

    monkeypatch.setattr(
        "app.api.product.product_service.create_product",
        fake_create_product
    )

    payload = {
        "startup_id": STARTUP_UUID,
        "name": "Meta Valley SaaS",
        "type": "saas",
        "last_updated_by": "cto",
    }

    response = client.post(
        "/products",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["last_updated_by"] == "cto"


def test_create_product_invalid_actor(
    client: TestClient,
    mock_authenticated_user
):
    """
    Apenas founder e CTO podem ser responsáveis pela atualização.
    """

    payload = {
        "startup_id": STARTUP_UUID,
        "name": "Meta Valley SaaS",
        "type": "saas",
        "last_updated_by": "cfo",
    }

    response = client.post(
        "/products",
        json=payload
    )

    assert response.status_code == 422


def test_get_products_by_startup(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_product_data
):
    """
    Testa a listagem de produtos de uma startup.
    """

    async def fake_get_products(startup_id, user_id):
        return [mock_product_data]

    monkeypatch.setattr(
        "app.api.product.product_service.get_products_by_startup",
        fake_get_products
    )

    response = client.get(
        f"/products/startup/{STARTUP_UUID}"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == PRODUCT_UUID
    assert data[0]["startup_id"] == STARTUP_UUID
    assert data[0]["name"] == "Meta Valley SaaS"


def test_get_product(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_product_data
):
    """
    Testa a busca de um produto específico.
    """

    async def fake_get_product(product_id, user_id):
        return mock_product_data

    monkeypatch.setattr(
        "app.api.product.product_service.get_product_by_id",
        fake_get_product
    )

    response = client.get(
        f"/products/{PRODUCT_UUID}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == PRODUCT_UUID
    assert data["name"] == "Meta Valley SaaS"
    assert data["last_updated_by"] == "founder"


def test_get_product_not_found(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Produto inexistente ou sem acesso deve retornar 404.
    """

    async def fake_get_product(product_id, user_id):
        return None

    monkeypatch.setattr(
        "app.api.product.product_service.get_product_by_id",
        fake_get_product
    )

    response = client.get(
        f"/products/{PRODUCT_UUID}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Produto não encontrado ou acesso negado."
    )


def test_update_product_by_founder(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_product_data
):
    """
    Testa alteração manual feita pelo founder.
    """

    updated_product = {
        **mock_product_data,
        "name": "Meta Valley SaaS Pro",
        "last_updated_by": "founder",
    }

    async def fake_update_product(product_id, user_id, payload):
        return updated_product

    monkeypatch.setattr(
        "app.api.product.product_service.update_product",
        fake_update_product
    )

    payload = {
        "name": "Meta Valley SaaS Pro",
        "last_updated_by": "founder",
    }

    response = client.patch(
        f"/products/{PRODUCT_UUID}",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Meta Valley SaaS Pro"
    assert data["last_updated_by"] == "founder"


def test_update_product_by_cto(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_product_data
):
    """
    Testa alteração persistida através do fluxo do CTO.
    """

    updated_product = {
        **mock_product_data,
        "description": "Descrição construída com auxílio do CTO.",
        "last_updated_by": "cto",
    }

    async def fake_update_product(product_id, user_id, payload):
        return updated_product

    monkeypatch.setattr(
        "app.api.product.product_service.update_product",
        fake_update_product
    )

    payload = {
        "description": "Descrição construída com auxílio do CTO.",
        "last_updated_by": "cto",
    }

    response = client.patch(
        f"/products/{PRODUCT_UUID}",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == (
        "Descrição construída com auxílio do CTO."
    )
    assert data["last_updated_by"] == "cto"


def test_update_product_invalid_actor(
    client: TestClient,
    mock_authenticated_user
):
    """
    CFO/CEO/CMO/etc. não podem ser informados como responsáveis
    pela atualização de um produto.
    """

    payload = {
        "name": "Produto alterado",
        "last_updated_by": "cfo",
    }

    response = client.patch(
        f"/products/{PRODUCT_UUID}",
        json=payload
    )

    assert response.status_code == 422


def test_delete_product(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user
):
    """
    Testa a deleção de um produto.
    """

    async def fake_delete_product(product_id, user_id):
        return True

    monkeypatch.setattr(
        "app.api.product.product_service.delete_product",
        fake_delete_product
    )

    response = client.delete(
        f"/products/{PRODUCT_UUID}"
    )

    assert response.status_code == 204
    
