from fastapi import Request, HTTPException, status, Depends
from supabase_auth import User
from supabase.client import Client

from app.core.supabase import get_supabase_client

async def get_current_user(
    request: Request,
    supabase_client: Client = Depends(get_supabase_client)
) -> User:
    # 1. Prefere o header para permitir que clientes cross-site ignorem cookies antigos.
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")
        if token and token.startswith("Bearer "):
            token = token.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido."
        )

    try:
        # 2. Valida o token no Supabase
        user_response = supabase_client.auth.get_user(token)
        
        # Proteção para o Pylance: verifica se user_response e user_response.user não são None
        if user_response is None or user_response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sessão inválida ou expirada."
            )

        return user_response.user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )