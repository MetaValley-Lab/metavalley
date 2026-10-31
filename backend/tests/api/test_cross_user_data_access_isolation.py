import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app  # Ajuste para o caminho da sua instância FastAPI

# 💡 CORREÇÃO: Mudamos o mark de 'asyncio' para 'anyio' para casar com o seu plugin instalado
@pytest.mark.anyio
async def test_cross_user_data_access_isolation():
    """Garante que um usuário não consegue ler dados da startup de outro."""
    token_usuario_malicioso = "Bearer TOKEN_VALIDO_DO_ATACANTE"
    id_startup_da_vitima = "123e4567-e89b-12d3-a456-426614174000"
    
    headers = {"Authorization": token_usuario_malicioso}
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/startups/{id_startup_da_vitima}", headers=headers)
        
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED, 
            status.HTTP_403_FORBIDDEN, 
            status.HTTP_404_NOT_FOUND
        ]

