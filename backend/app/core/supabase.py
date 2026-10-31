from fastapi import Request
from supabase import acreate_client, AsyncClient, AsyncClientOptions 
from app.core.config import settings


async def get_admin_supabase_client() -> AsyncClient:
    return await acreate_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_KEY
    )
    

async def get_supabase_client(request: Request) -> AsyncClient:
    auth_header = request.headers.get("Authorization")
    token = None

    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header[7:].strip()
    else:
        token = request.cookies.get("access_token")
        if token and token.lower().startswith("bearer "):
            token = token[7:].strip()
            
    options = None
    if token:
        options = AsyncClientOptions(
            headers={"Authorization": f"Bearer {token}"}
        )
    
    return await acreate_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_KEY,
        options=options
    )
    
