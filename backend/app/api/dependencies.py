import asyncio
from fastapi import Request, HTTPException, status, Depends
from supabase_auth import User
from supabase import AsyncClient

from httpx import HTTPError, TimeoutException 
from postgrest.exceptions import APIError

from app.core.supabase import get_supabase_client

async def get_current_user(
    request: Request,
    supabase_client: AsyncClient = Depends(get_supabase_client)
) -> User:
    auth_header = request.headers.get("Authorization")
    token = None

    # --- PROBLEMA 2 e 3: Tratamento estrito do Authorization Header e Cookies ---
    if auth_header:
        # Permite 'bearer ' ou 'Bearer ' (case-insensitive)
        if not auth_header.lower().startswith("bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cabeçalho Authorization malformado. Deve iniciar com 'Bearer '."
            )
        
        token = auth_header[7:].strip() # Remove 'bearer ' ou 'Bearer ' de forma segura
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Bearer está vazio no cabeçalho Authorization."
            )
    else:
        # Só recorre ao cookie se o cabeçalho Authorization NÃO estiver presente
        token = request.cookies.get("access_token")
        
        if token:
            # Se o token do cookie vier prefixado com Bearer por engano, limpa de forma segura
            if token.lower().startswith("bearer "):
                token = token[7:].strip()
            
            # TODO
            # NOTA DE SEGURANÇA (PROBLEMA 3):
            # Se a autenticação veio por cookie, você DEVE validar o token CSRF nas rotas de mutação (POST, PUT, DELETE).
            # Como GET é idempotente, permitimos a extração aqui, mas proteja seus métodos inseguros.

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido."
        )

    # --- PROBLEMA 1 e 4: Validação sem bloquear Event Loop e Erros de Infraestrutura ---
    try:
        # Executa a chamada síncrona do Supabase em um pool de threads do FastAPI/Asyncio
        user_response = await supabase_client.auth.get_user(token)
        
        if user_response is None or user_response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sessão inválida ou expirada."
            )

        return user_response.user

    except HTTPException:
        # Repassa exceções HTTP geradas explicitamente por nós ou pelo fluxo
        raise

    except (HTTPError, TimeoutException, APIError) as infra_err:
        # Captura falhas de conexão, timeouts ou problemas no servidor do Supabase
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de autenticação temporariamente indisponível. Tente novamente mais tarde."
        )

    except Exception as e:
        # Captura erros reais de credenciais inválidas ou erros inesperados de código
        # Nota: Se o SDK do Supabase lançar uma exceção específica para token inválido, capture-a antes desta.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )
