from fastapi import APIRouter, HTTPException, Response, status, Depends, Request
from supabase_auth import User

from app.core.config import settings
from app.core.exceptions import InvalidCredentialsException, UserRegistrationException
from app.schemas.auth_schema import UserLogin, UserRegister, ChangePasswordSchema, ForgotPassword, ResetPasswordRequest
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user
from app.core.limiter import limiter


router = APIRouter(prefix="/auth", tags=["Autenticação"])

auth_service = AuthService()

@router.post(
    "/login", 
    summary="Realiza login e define cookie de sessão"
)
@limiter.limit("5/minute")
async def login(request: Request, user: UserLogin, response: Response):
    try:
        session, auth_user = await auth_service.authenticate_user(user)
        
        access_token = session.access_token
        refresh_token = session.refresh_token
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=settings.IS_PRODUCTION,
            samesite="lax",
            max_age=3600,
            path="/"
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.IS_PRODUCTION,
            samesite="lax",
            max_age=60*60*24*30,
            path="/"
        )
        
        
        return {
            "message": "Login feito com sucesso",
            "user": { "id": auth_user.id, "email": auth_user.email }
        }
        
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
    
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Realizar o cadastro da conta"
)
async def register(user: UserRegister):
    try:
        
        return await auth_service.register_user(user)
    
    except UserRegistrationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except HTTPException:
            raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro inesperado no servidor."
        )
        

@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user),
):
    return current_user


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Solicitar e-mail de recuperação de senha"
)
async def forgot_password(payload: ForgotPassword):
    return await auth_service.request_password_reset(email=payload.email)


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Redefinir senha usando o código recebido por e-mail"
)
async def reset_password(payload: ResetPasswordRequest):
    try:
        return await auth_service.reset_password(
            code=payload.code,
            access_token=payload.access_token,
            refresh_token=payload.refresh_token,
            new_password=payload.new_password
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    payload: ChangePasswordSchema,
    current_user: User = Depends(get_current_user)
):
    try:
        return await auth_service.change_password(
            email=str(current_user.email),
            current_password=payload.current_password,
            new_password=payload.new_password
        )
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
