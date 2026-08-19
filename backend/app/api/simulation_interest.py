from fastapi import APIRouter, Depends, HTTPException, status
from supabase_auth import User

from app.api.dependencies import get_current_user
from app.schemas.simulation_interest_schema import (
    SimulationInterestCreate,
    SimulationInterestResponse,
    SimulationInterestStatusResponse,
)
from app.services.simulation_interest_service import SimulationInterestService


router = APIRouter(
    prefix="/simulation-interests",
    tags=["Simulation Interests"]
)

simulation_interest_service = SimulationInterestService()


@router.post(
    "",
    response_model=SimulationInterestResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_simulation_interest(
    payload: SimulationInterestCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        return await simulation_interest_service.create_interest(
            user_id=str(current_user.id),
            email=str(current_user.email),
            payload=payload
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/startup/{startup_id}/me",
    response_model=SimulationInterestStatusResponse
)
async def get_my_simulation_interest(
    startup_id: str,
    current_user: User = Depends(get_current_user)
):
    interested = await simulation_interest_service.has_user_interest(
        user_id=str(current_user.id),
        startup_id=startup_id
    )

    return SimulationInterestStatusResponse(
        interested=interested
    )


@router.delete(
    "/{interest_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_simulation_interest(
    interest_id: str,
    current_user: User = Depends(get_current_user)
):
    deleted = await simulation_interest_service.delete_interest(
        interest_id=interest_id,
        user_id=str(current_user.id)
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interesse não encontrado ou acesso negado."
        )
        
