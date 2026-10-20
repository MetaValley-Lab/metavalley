import asyncio
import os
import pytest
from types import SimpleNamespace

from app.api.dependencies import get_current_user
from app.core.limiter import limiter

os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "dummy-key")
os.environ.setdefault("IS_PRODUCTION", "false")


from app.core.exceptions import InvalidCredentialsException, UserRegistrationException
from app.main import app
from app.core.supabase import supabase
from app.services.auth_service import AuthService


def test_auth_routes_are_registered(client):
    schema = app.openapi()
    paths = schema.get("paths", {}).keys()

    assert "/auth/login" in paths
    assert "/auth/register" in paths


def test_health_endpoint_is_available(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_endpoint_success_sets_cookies_and_returns_user_without_tokens(client, monkeypatch):
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
    assert "access_token" not in body
    assert "refresh_token" not in body
    assert body["user"] == {"id": "user-123", "email": "user@example.com"}

    set_cookie_value = response.headers.get("set-cookie", "")
    assert "access_token=test-access-token" in set_cookie_value
    assert "refresh_token=test-refresh-token" in set_cookie_value
    assert "httponly" in set_cookie_value.lower()


def test_login_endpoint_invalid_credentials_returns_401(client, monkeypatch):
    async def fake_authenticate_user(user):
        raise InvalidCredentialsException("E-mail ou senha inválidos")

    monkeypatch.setattr("app.api.auth.auth_service.authenticate_user", fake_authenticate_user)

    
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "senhaerrada",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha inválidos"


def test_reset_password_with_code_exchanges_session_before_updating_user(monkeypatch):
    calls = []

    def fake_exchange_code(params):
        calls.append(("exchange", params))
        return SimpleNamespace(session=object())

    def fake_update_user(attributes):
        calls.append(("update", attributes))

    monkeypatch.setattr(supabase.auth, "exchange_code_for_session", fake_exchange_code)
    monkeypatch.setattr(supabase.auth, "update_user", fake_update_user)

    result = asyncio.run(
        AuthService().reset_password(
            code="recovery-code",
            new_password="nova-senha-segura",
        )
    )

    assert result == {"message": "Senha restaurada com sucesso."}
    assert calls == [
        (
            "exchange",
            {
                "auth_code": "recovery-code",
                "code_verifier": "",
                "redirect_to": "",
            },
        ),
        ("update", {"password": "nova-senha-segura"}),
    ]


def test_reset_password_with_hash_credentials_sets_session_before_updating_user(monkeypatch):
    calls = []

    def fake_set_session(access_token, refresh_token):
        calls.append(("set_session", access_token, refresh_token))
        return SimpleNamespace(session=object())

    def fake_update_user(attributes):
        calls.append(("update", attributes))

    monkeypatch.setattr(supabase.auth, "set_session", fake_set_session)
    monkeypatch.setattr(supabase.auth, "update_user", fake_update_user)

    result = asyncio.run(
        AuthService().reset_password(
            code=None,
            access_token="access",
            refresh_token="refresh",
            new_password="nova-senha-segura",
        )
    )

    assert result == {"message": "Senha restaurada com sucesso."}
    assert calls == [
        ("set_session", "access", "refresh"),
        ("update", {"password": "nova-senha-segura"}),
    ]


@pytest.mark.parametrize(
    "credentials",
    [
        {},
        {"access_token": "access"},
        {"refresh_token": "refresh"},
        {"code": "code", "access_token": "access", "refresh_token": "refresh"},
    ],
)
def test_reset_password_rejects_incomplete_or_mixed_credentials(client, credentials):
    response = client.post(
        "/auth/reset-password",
        json={"new_password": "nova-senha-segura", **credentials},
    )

    assert response.status_code == 422


def test_register_endpoint_success_creates_account_without_db(client, monkeypatch):
    async def fake_register_user(user):
        return {
            "message": "Usuário criado com sucesso.",
            "user": {
                "id": "created-user-456",
                "email": user.email,
            },
        }

    monkeypatch.setattr("app.api.auth.auth_service.register_user", fake_register_user)

    
    
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


def test_login_rate_limit_exceeded(client, monkeypatch):
    # Reseta o histórico de requisições de testes anteriores
    try:
        limiter.reset()
    except Exception:
        limiter._storage.reset()

    # Mock para não bater na regra de autenticação real
    async def fake_authenticate_user(user):
        raise InvalidCredentialsException("E-mail ou senha inválidos")

    monkeypatch.setattr("app.api.auth.auth_service.authenticate_user", fake_authenticate_user)

    payload = {"email": "user@example.com", "password": "senhaerrada"}

    # Realiza as 5 tentativas permitidas na janela de tempo
    for _ in range(5):
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 401

    # A 6ª tentativa deve estourar o limite e retornar 429
    response_blocked = client.post("/auth/login", json=payload)
    assert response_blocked.status_code == 429
    
