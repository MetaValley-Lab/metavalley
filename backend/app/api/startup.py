from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from supabase_auth import User

from app.api.dependencies import get_current_user
from app.schemas.startup_schema import StartupCreate, StartupResponse, StartupUpdate
from app.services.startup_service import StartupService

router = APIRouter(prefix="/startups", tags=["Startups"])
startup_service = StartupService()


@router.post("", response_model=StartupResponse, status_code=status.HTTP_201_CREATED)
async def create_startup(
    payload: StartupCreate,
    current_user: User = Depends(get_current_user)
):
    return await startup_service.create_startup(user_id=str(current_user.id), payload=payload)


@router.get("", response_model=List[StartupResponse])
async def get_my_startups(
    current_user: User = Depends(get_current_user)
):
    return await startup_service.get_user_startups(user_id=str(current_user.id))


@router.get("/{startup_id}", response_model=StartupResponse)
async def get_startup(
    startup_id: str,
    current_user: User = Depends(get_current_user)
):
    startup = await startup_service.get_startup_by_id(
        startup_id=startup_id, 
        user_id=str(current_user.id)
    )
    if not startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Startup não encontrada."
        )
    return startup


@router.patch("/{startup_id}", response_model=StartupResponse)
async def update_startup(
    startup_id: str,
    payload: StartupUpdate,
    current_user: User = Depends(get_current_user)
):
    updated = await startup_service.update_startup(
        startup_id=startup_id,
        user_id=str(current_user.id),
        payload=payload
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Startup não encontrada."
        )
    return updated


@router.delete("/{startup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_startup(
    startup_id: str,
    current_user: User = Depends(get_current_user)
):
    deleted = await startup_service.delete_startup(
        startup_id=startup_id, 
        user_id=str(current_user.id)
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Startup não encontrada."
        )