from gotrue.errors import AuthApiError

from schemas.auth_schema import UserLogin, UserRegister
from core.supabase import supabase
from core.exceptions import InvalidCredentialsException, AuthException, UserRegistrationException



class AuthService:
    
    async def autenticate_user(self, user: UserLogin):
        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": user.email,
                "password": user.password
            })
            
            session = auth_response.session
            auth_user = auth_response.user
            
            if session is None or auth_user is None:
                raise InvalidCredentialsException("Sessão ou usuários não forma retornados.")
                
            return session, auth_user
        except AuthException:
            raise InvalidCredentialsException("E-mail ou senha inválidos")
        except Exception as e:
            if isinstance(e, InvalidCredentialsException):
                raise
            raise InvalidCredentialsException("Erro no processo de autenticação.")
            
    
    async def register_user(self, user: UserRegister):
        try:
            auth_response = supabase.auth.sign_up({
                "email": user.email,
                "password": user.password,
                "options": {
                    "data": {
                        "username": user.username,
                        "phone_number": user.phone_number
                    }
                }
            })
            
            auth_user = auth_response.user
            if auth_user is None:
                raise UserRegistrationException("Não foi possível criar o usuário.")
            
            return {
                "message": "Usuário criado com sucesso.",
                "user": {
                    "id": auth_user.id,
                    "email": auth_user.email
                }
            }
        except AuthApiError as e:
            raise UserRegistrationException(f"Falha ao cadastrar usuário: {e.message}")
        except Exception as e:
            if isinstance(e, UserRegistrationException):
                raise
            raise UserRegistrationException("Ocorreu um erro interno ao criar um usuário.")
        
        