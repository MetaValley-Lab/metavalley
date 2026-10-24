from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from supabase_auth import User
from supabase.client import Client

from app.api.dependencies import get_current_user
from app.schemas.startup_schema import StartupCreate, StartupResponse, StartupUpdate
from app.services.startup_service import StartupService
from app.core.supabase import get_supabase_client

router = APIRouter(prefix="/startups", tags=["Startups"])


@router.post("", response_model=StartupResponse, status_code=status.HTTP_201_CREATED)
async def create_startup(
    request: Request,
    payload: StartupCreate,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    startup_service = StartupService(supabase_client)
    return await startup_service.create_startup(user_id=str(current_user.id), payload=payload)


@router.get("", response_model=List[StartupResponse])
async def get_my_startups(
    request: Request,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    # ⚡️ Injeta o token de autenticação no cliente para satisfazer as regras de RLS do banco
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)

    startup_service = StartupService(supabase_client)
    
    return await startup_service.get_user_startups(user_id=str(current_user.id))


@router.get("/{startup_id}", response_model=StartupResponse)
async def get_startup(
    request: Request,
    startup_id: str,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    startup_service = StartupService(supabase_client)
    startup = await startup_service.get_startup_by_id(
        startup_id=startup_id, 
        user_id=str(current_user.id)
    )
    print(f"[DEBUGIN STARTUP]: {startup}")
    if not startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Startup não encontrada."
        )
    return startup


@router.patch("/{startup_id}", response_model=StartupResponse)
async def update_startup(
    request: Request,
    startup_id: str,
    payload: StartupUpdate,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    startup_service = StartupService(supabase_client)
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


@router.post("/{startup_id}/image", response_model=StartupResponse)
async def upload_startup_image(
    request: Request,
    startup_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    try:
        startup_service = StartupService(supabase_client)
        startup = await startup_service.upload_startup_image(
            startup_id=startup_id,
            user_id=str(current_user.id),
            file=file,
            supabase_client=supabase_client
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup não encontrada.")
    return startup


@router.delete("/{startup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_startup(
    request: Request,
    startup_id: str,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    startup_service = StartupService(supabase_client)
    deleted = await startup_service.delete_startup(
        startup_id=startup_id, 
        user_id=str(current_user.id)
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Startup não encontrada."
        )
        
        