from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from supabase_auth import User

from app.services.user_service import UserService
from app.api.dependencies import get_current_user
from app.core.exceptions import UserRegistrationException, UserEditException
from app.schemas.user_schema import UserEditProfileRequest

router = APIRouter(prefix="/user", tags=["User"])
user_service = UserService()


@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_profile(current_user: User = Depends(get_current_user)):
    profile = await user_service.get_profile(user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")
    return profile

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
        
        
@router.patch(
    "/edit-profile",
    status_code=status.HTTP_200_OK,
    summary="Endpoint responsável por editar informações do usupario"
)
async def edit_profile(
    profile_edits: UserEditProfileRequest,
    current_user: User = Depends(get_current_user)
):
    
    try:
        return await user_service.edit_profile(
            user_id=current_user.id,
            profile_edits=profile_edits
        )
    except UserEditException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a solicitação."
        )


@router.post("/avatar", status_code=status.HTTP_200_OK)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    try:
        profile = await user_service.upload_avatar(user_id=current_user.id, file=file)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")
        return profile
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserEditException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
