from supabase import acreate_client, AsyncClient
from app.core.config import settings


async def get_supabase_client() -> AsyncClient:
    return await acreate_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_KEY
    )
    
