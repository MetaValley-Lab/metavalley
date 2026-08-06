from fastapi import APIRouter, HTTPException, Response, status

from core.config import settings

from core.exceptions import InvalidCredentialsException, UserRegistrationException

from schemas.auth_schema import UserLogin, UserRegister

from services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Autenticação"])

auth_service = AuthService()

@router.post(
    "/login", 
    summary="Realiza login e define cookie de sessão"
)
async def login(user: UserLogin, response: Response):
    try:
        session, auth_user = await auth_service.autenticate_user(user)
        
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
            key="refrest_token",
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
        return HTTPException(
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
        
