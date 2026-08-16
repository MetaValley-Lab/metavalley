from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from supabase_auth import User

from app.api.dependencies import get_current_user
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

canvas_zone_service = CanvasZoneService()


@router.post(
    "",
    response_model=CanvasZoneResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_canvas_zone(
    payload: CanvasZoneCreate,
    current_user: User = Depends(get_current_user)
):
    try:
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
    startup_id: UUID,
    current_user: User = Depends(get_current_user)
):
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
    zone_id: UUID,
    current_user: User = Depends(get_current_user)
):
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
    zone_id: UUID,
    payload: CanvasZoneUpdate,
    current_user: User = Depends(get_current_user)
):
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
    zone_id: UUID,
    current_user: User = Depends(get_current_user)
):
    deleted = await canvas_zone_service.delete_zone(
        zone_id=str(zone_id),
        user_id=str(current_user.id)
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canvas Zone não encontrada ou acesso negado."
        )
        
    