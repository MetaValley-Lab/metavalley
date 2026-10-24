from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from supabase_auth import User
from supabase.client import Client

from app.services.user_service import UserService
from app.api.dependencies import get_current_user
from app.core.exceptions import UserRegistrationException, UserEditException
from app.schemas.user_schema import UserEditProfileRequest
from app.core.supabase import get_supabase_client

router = APIRouter(prefix="/user", tags=["User"])



@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_profile(
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client),
    request: Request = None # Certifique-se de importar Request do fastapi se necessário
):
    # ⚡️ EXTRAI O TOKEN DO USUÁRIO CORRENTE (dos cookies ou do header)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")
        if token and token.startswith("Bearer "):
            token = token.removeprefix("Bearer ").strip()

    # ⚡️ AJUSTE CRÍTICO: Vincula o token do usuário logado nesta instância do cliente
    if token:
        supabase_client.postgrest.auth(token)

    user_service = UserService(supabase_client)
    profile = await user_service.get_profile(user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")
    return profile


@router.patch(
    "/onboarding/complete",
    status_code=status.HTTP_200_OK,
    summary="Marca o onboarding do usuário como concluído"
)
async def completed_onboarding(
    request: Request,
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
        user_service = UserService(supabase_client)
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
    request: Request,
    profile_edits: UserEditProfileRequest,
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
        user_service = UserService(supabase_client)
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
    request: Request,
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
        user_service = UserService(supabase_client)
        profile = await user_service.upload_avatar(user_id=current_user.id, file=file, supabase_client=supabase_client)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")
        return profile
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserEditException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
