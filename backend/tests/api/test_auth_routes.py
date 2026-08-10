import os
import pytest
from types import SimpleNamespace

from app.api.dependencies import get_current_user

os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "dummy-key")
os.environ.setdefault("IS_PRODUCTION", "false")


from app.core.exceptions import InvalidCredentialsException, UserRegistrationException
from app.main import app


def test_auth_routes_are_registered(client):
    schema = app.openapi()
    paths = schema.get("paths", {}).keys()

    assert "/auth/login" in paths
    assert "/auth/register" in paths


def test_health_endpoint_is_available(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_endpoint_success_sets_cookies_and_returns_user(client, monkeypatch):
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
    assert body["user"] == {"id": "user-123", "email": "user@example.com"}

    set_cookie_value = response.headers.get("set-cookie", "")
    assert "access_token=test-access-token" in set_cookie_value
    assert "refresh_token=test-refresh-token" in set_cookie_value


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


def test_register_endpoint_business_error_returns_400(client, monkeypatch):
    async def fake_register_user(user):
        raise UserRegistrationException("Falha ao cadastrar usuário: E-mail já existente")

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

    assert response.status_code == 400
    assert response.json()["detail"] == "Falha ao cadastrar usuário: E-mail já existente"


    # --- 1. Testes de Esqueci / Redefinir Senha ---

def test_forgot_password_always_returns_200(client, monkeypatch):
    async def fake_request_reset(email):
        return {"message": "Se esse e-mail existir na nossa base, as instruções de recuperação foram enviadas."}

    monkeypatch.setattr("app.api.auth.auth_service.request_password_reset", fake_request_reset)

    response = client.post("/auth/forgot-password", json={"email": "teste@example.com"})

    assert response.status_code == 200
    assert "instruções de recuperação foram enviadas" in response.json()["message"]


def test_reset_password_success(client, monkeypatch):
    async def fake_reset_password(code, new_password):
        return {"message": "Senha redefinida com sucesso."}

    monkeypatch.setattr("app.api.auth.auth_service.reset_password", fake_reset_password)

    response = client.post(
        "/auth/reset-password",
        json={"code": "valid-code-123", "new_password": "nova_senha_segura"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Senha redefinida com sucesso."


def test_reset_password_invalid_code_returns_400(client, monkeypatch):
    async def fake_reset_password(code, new_password):
        raise InvalidCredentialsException("Código de recuperação inválido ou expirado.")

    monkeypatch.setattr("app.api.auth.auth_service.reset_password", fake_reset_password)

    response = client.post(
        "/auth/reset-password",
        json={"code": "expired-code", "new_password": "nova_senha_segura"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Código de recuperação inválido ou expirado."


# --- 2. Testes de Rotas Autenticadas (Usando Dependency Override) ---

@pytest.fixture
def mock_authenticated_user():
    """Sobrescreve a dependência get_current_user para simular usuário logado."""
    fake_user = SimpleNamespace(id="user-uuid-123", email="logged_user@example.com")
    app.dependency_overrides[get_current_user] = lambda: fake_user
    yield fake_user
    app.dependency_overrides.clear()  # Limpa o override após o teste


def test_change_password_success(client, monkeypatch, mock_authenticated_user):
    # Alterado o nome do primeiro parâmetro de 'user_email' para 'email'
    async def fake_change_password(email, current_password, new_password):
        return {"message": "Senha alterada com sucesso."}

    monkeypatch.setattr("app.api.auth.auth_service.change_password", fake_change_password)

    response = client.post(
        "/auth/change-password",
        json={"current_password": "senha_antiga", "new_password": "senha_nova_123"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Senha alterada com sucesso."


def test_complete_onboarding_success(client, monkeypatch, mock_authenticated_user):
    async def fake_complete_onboarding(user_id):
        return {
            "message": "Onboarding concluído com sucesso.",
            "onboarding_completed": True
        }

    monkeypatch.setattr("app.api.user.user_service.complete_onboarding", fake_complete_onboarding)

    response = client.patch("/user/onboarding/complete")

    assert response.status_code == 200
    assert response.json()["onboarding_completed"] is True
    
    