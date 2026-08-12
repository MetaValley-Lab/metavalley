from fastapi import APIRouter, Depends
from supabase_auth import User

from app.api.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat agents"])


@router.post("/{agent_ai}")
async def chat(agent_ai: str, message: str, user: User = Depends(get_current_user)):
    ...
