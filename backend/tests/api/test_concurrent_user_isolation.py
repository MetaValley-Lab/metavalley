import pytest
import anyio
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from fastapi import status, Request
from app.main import app
from app.api.dependencies import get_current_user
from app.core.supabase import get_supabase_client
from supabase_auth import User

# 1. Usuários Mockados válidos com Pydantic v2
mock_user_a = User.model_validate({
    "id": "user-aaa-1111",
    "email": "user_a@test.com",
    "aud": "authenticated",
    "created_at": "2026-10-31T00:00:00Z",
    "app_metadata": {"provider": "email"},
    "user_metadata": {}
})

mock_user_b = User.model_validate({
    "id": "user-bbb-2222",
    "email": "user_b@test.com",
    "aud": "authenticated",
    "created_at": "2026-10-31T00:00:00Z",
    "app_metadata": {"provider": "email"},
    "user_metadata": {}
})

# 2. Overrides das dependências do FastAPI
async def override_get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header == "Bearer TOKEN_MOCK_A":
        return mock_user_a
    if auth_header == "Bearer TOKEN_MOCK_B":
        return mock_user_b
    from fastapi import HTTPException
    raise HTTPException(status_code=401, detail="Token inválido")

async def override_get_supabase_client(request: Request):
    """
    Cria um cliente Supabase Mock estruturado com UUIDs válidos e metadados
    obrigatórios para passar sem erros no serialize_response (StartupResponse).
    """
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_select = MagicMock()
    mock_eq = MagicMock()
    
    # 💡 CORREÇÃO: Usando UUID estrutural válido e chaves obrigatórias exigidas pelo Pydantic
    mock_execute = AsyncMock()
    mock_execute.return_value = MagicMock(data=[{
        "id": "123e4567-e89b-12d3-a456-426614174000", # UUID válido
        "user_id": "123e4567-e89b-12d3-a456-426614174111",
        "name": "Test Startup",
        "description": "Uma startup de IA simulada concorrentemente",
        "status": "active",
        "stage": "idea",
        "created_at": "2026-10-31T00:00:00Z",
        "updated_at": "2026-10-31T00:00:00Z"
    }])
    
    mock_client.table.return_value = mock_table
    mock_table.select.return_value = mock_select
    mock_select.eq.return_value = mock_eq
    mock_eq.execute = mock_execute
    
    return mock_client


@pytest.mark.anyio
async def test_concurrent_requests_do_not_leak_auth_state():
    """
    Força requisições paralelas simultâneas e garante que cada escopo
    de dependência resolva os dados sem vazamento de estado.
    """
    # Injeta os mocks na aplicação FastAPI
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_supabase_client] = override_get_supabase_client

    async def request_user_a(client: AsyncClient):
        headers = {"Authorization": "Bearer TOKEN_MOCK_A"}
        response = await client.get("/startups", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        # Garante que os dados retornaram corretos da nossa estrutura mockada
        assert "Test Startup" in response.text

    async def request_user_b(client: AsyncClient):
        headers = {"Authorization": "Bearer TOKEN_MOCK_B"}
        response = await client.get("/startups", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert "Test Startup" in response.text

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        async with anyio.create_task_group() as tg:
            tg.start_soon(request_user_a, client)
            tg.start_soon(request_user_b, client)

    # Limpa os overrides para não afetar outros testes do projeto
    app.dependency_overrides.clear()

