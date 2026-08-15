from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from supabase_auth import User

from app.api.dependencies import get_current_user
from app.schemas.planning_item_schema import PlanningItemCreate, PlanningItemResponse, PlanningItemUpdate
from app.services.planning_item_service import PlanningItemService

router = APIRouter(prefix="/planning-items", tags=["Planning Items"])
planning_service = PlanningItemService()


@router.post("", response_model=PlanningItemResponse, status_code=status.HTTP_201_CREATED)
async def create_planning_item(
    payload: PlanningItemCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        return await planning_service.create_item(user_id=str(current_user.id), payload=payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/startup/{startup_id}", response_model=List[PlanningItemResponse])
async def get_startup_planning_items(
    startup_id: UUID,
    current_user: User = Depends(get_current_user)
):
    return await planning_service.get_items_by_startup(
        startup_id=str(startup_id), 
        user_id=str(current_user.id)
    )


@router.patch("/{item_id}", response_model=PlanningItemResponse)
async def update_planning_item(
    item_id: UUID,
    payload: PlanningItemUpdate,
    current_user: User = Depends(get_current_user)
):
    updated = await planning_service.update_item(
        item_id=str(item_id),
        user_id=str(current_user.id),
        payload=payload
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Planning item não encontrado ou acesso negado."
        )
    return updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_planning_item(
    item_id: UUID,
    current_user: User = Depends(get_current_user)
):
    deleted = await planning_service.delete_item(
        item_id=str(item_id), 
        user_id=str(current_user.id)
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Planning item não encontrado ou acesso negado."
        )
        
        
