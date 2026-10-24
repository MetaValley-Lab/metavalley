from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Request
from supabase_auth import User
from supabase.client import Client

from app.api.dependencies import get_current_user
from app.core.supabase import get_supabase_client
from app.schemas.canvas_zone_schema import (
    CanvasZoneCreate,
    CanvasZoneResponse,
    CanvasZoneUpdate,
)
from app.services.canvas_zone_service import CanvasZoneService


router = APIRouter(
    prefix="/canvas-zones",
    tags=["Canvas Zones"]
)


@router.post(
    "",
    response_model=CanvasZoneResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_canvas_zone(
    request: Request,
    payload: CanvasZoneCreate,
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
        canvas_zone_service = CanvasZoneService(supabase_client)
        return await canvas_zone_service.create_zone(
            user_id=str(current_user.id),
            payload=payload
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get(
    "/startup/{startup_id}",
    response_model=List[CanvasZoneResponse]
)
async def get_startup_canvas_zones(
    request: Request,
    startup_id: UUID,
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
    canvas_zone_service = CanvasZoneService(supabase_client)
    zones = await canvas_zone_service.get_zones_by_startup(
        startup_id=str(startup_id),
        user_id=str(current_user.id)
    )

    return zones


@router.get(
    "/{zone_id}",
    response_model=CanvasZoneResponse
)
async def get_canvas_zone(
    request: Request,
    zone_id: UUID,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    canvas_zone_service = CanvasZoneService(supabase_client)
    zone = await canvas_zone_service.get_zone_by_id(
        zone_id=str(zone_id),
        user_id=str(current_user.id)
    )

    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canvas Zone não encontrada ou acesso negado."
        )

    return zone


@router.patch(
    "/{zone_id}",
    response_model=CanvasZoneResponse
)
async def update_canvas_zone(
    request: Request,
    zone_id: UUID,
    payload: CanvasZoneUpdate,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    canvas_zone_service = CanvasZoneService(supabase_client)
    updated = await canvas_zone_service.update_zone(
        zone_id=str(zone_id),
        user_id=str(current_user.id),
        payload=payload
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canvas Zone não encontrada ou acesso negado."
        )

    return updated


@router.delete(
    "/{zone_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_canvas_zone(
    request: Request,
    zone_id: UUID,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    canvas_zone_service = CanvasZoneService(supabase_client)
    deleted = await canvas_zone_service.delete_zone(
        zone_id=str(zone_id),
        user_id=str(current_user.id)
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canvas Zone não encontrada ou acesso negado."
        )
        
    