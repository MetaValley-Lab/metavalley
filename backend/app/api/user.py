from fastapi import APIRouter, status, Depends, HTTPException
from supabase_auth import User

from app.services.user_service import UserService
from app.api.dependencies import get_current_user
from app.core.exceptions import UserRegistrationException

router = APIRouter(prefix="/user", tags=["User"])
user_service = UserService()

@router.patch(
    "/onboarding/complete",
    status_code=status.HTTP_200_OK,
    summary="Marca o onboarding do usuário como concluído"
)
async def completed_onboarding(current_user: User = Depends(get_current_user)):
    
    try:
        return await user_service.complete_onboarding(user_id=current_user.id)
    
    except UserRegistrationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a solicitação."
        )