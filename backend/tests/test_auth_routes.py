import os
from types import SimpleNamespace

os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "dummy-key")
os.environ.setdefault("IS_PRODUCTION", "false")

from fastapi.testclient import TestClient

from app.core.exceptions import InvalidCredentialsException, UserRegistrationException
from app.main import app


def test_auth_routes_are_registered():
    schema = app.openapi()
    paths = schema.get("paths", {}).keys()

    assert "/auth/login" in paths
    assert "/auth/register" in paths


def test_health_endpoint_is_available():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_endpoint_success_sets_cookies_and_returns_user(monkeypatch):
    async def fake_authenticate_user(user):
        session = SimpleNamespace(
            access_token="test-access-token",
            refresh_token="test-refresh-token",
        )
        auth_user = SimpleNamespace(
            id="user-123",
            email=user.email,
        )
        return session, auth_user

    monkeypatch.setattr("app.api.auth.auth_service.authenticate_user", fake_authenticate_user)

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "senha123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Login feito com sucesso"
    assert body["user"] == {"id": "user-123", "email": "user@example.com"}

    set_cookie_value = response.headers.get("set-cookie", "")
    assert "access_token=test-access-token" in set_cookie_value
    assert "refrest_token=test-refresh-token" in set_cookie_value


def test_login_endpoint_invalid_credentials_returns_401(monkeypatch):
    async def fake_authenticate_user(user):
        raise InvalidCredentialsException("E-mail ou senha inválidos")

    monkeypatch.setattr("app.api.auth.auth_service.authenticate_user", fake_authenticate_user)

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "senhaerrada",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha inválidos"


def test_register_endpoint_success_creates_account_without_db(monkeypatch):
    async def fake_register_user(user):
        return {
            "message": "Usuário criado com sucesso.",
            "user": {
                "id": "created-user-456",
                "email": user.email,
            },
        }

    monkeypatch.setattr("app.api.auth.auth_service.register_user", fake_register_user)

    client = TestClient(app)
    response = client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "senha123",
            "phone_number": "+5511999998888",
        },
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Usuário criado com sucesso."
    assert response.json()["user"]["email"] == "alice@example.com"


def test_register_endpoint_business_error_returns_400(monkeypatch):
    async def fake_register_user(user):
        raise UserRegistrationException("Falha ao cadastrar usuário: E-mail já existente")

    monkeypatch.setattr("app.api.auth.auth_service.register_user", fake_register_user)

    client = TestClient(app)
    response = client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "senha123",
            "phone_number": "+5511999998888",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Falha ao cadastrar usuário: E-mail já existente"
