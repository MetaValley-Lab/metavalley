import os
from supabase_auth.errors import AuthApiError
from dotenv import load_dotenv


from app.schemas.auth_schema import UserLogin, UserRegister
from app.core.supabase import supabase
from app.core.exceptions import InvalidCredentialsException, AuthException, UserRegistrationException

load_dotenv()

BASE_URL = str(os.getenv("BASE_URL"))

class AuthService:
    
    async def authenticate_user(self, user: UserLogin):
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
                raise e 
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
                raise e
            raise UserRegistrationException("Erro interno no processo de autenticação.")
        
        
    async def request_password_reset(self, email: str):
        try:
            supabase.auth.reset_password_for_email(
                email=email,
                options={
                    "redirect_to": f"{BASE_URL}/reset-password"
                }
            )
            
            return {
                "message": "Se esse e-mail existir na nossa base, as instruções de recuperação foram enviadas."
            }
        except Exception as e:
            print(f"❌ Erro ao solicitar reset de senha: {e}")
            return {
                "message": "Se esse e-mail existir na nossa base, as instruções de recuperação foram enviadas."
            }
            
            
    async def reset_password(
        self,
        code: str | None,
        new_password: str,
        access_token: str | None = None,
        refresh_token: str | None = None,
    ):
        try:
            if access_token and refresh_token:
                session_response = supabase.auth.set_session(
                    access_token,
                    refresh_token,
                )
            elif code:
                session_response = supabase.auth.exchange_code_for_session({
                    "auth_code": code,
                    "code_verifier": "",
                    "redirect_to": ""
                })
            else:
                raise InvalidCredentialsException("Código de restauração ausente.")
            
            if not session_response or not session_response.session:
                raise InvalidCredentialsException("Código de restauração de senha inválido ou expirado.")
            
            supabase.auth.update_user({"password": new_password})
            
            return {"message": "Senha restaurada com sucesso."}
            
        except Exception:
            raise InvalidCredentialsException("Erro ao restaurar a senha. Solicite um novo link.")
        
    
    async def change_password(self, email: str, current_password: str, new_password):
        try:
            reauth = supabase.auth.sign_in_with_password({
                "email": email,
                "password": current_password
            })
            
            if not reauth.user:
                raise InvalidCredentialsException("A senha atual fornecida está incorreta.")
            
            supabase.auth.update_user({
                "password": new_password
            })
            
            return {"message": "Senha atualizada com sucesso"}
            
        except AuthApiError:
            raise InvalidCredentialsException("A senha atual informada está incorreta.")
        except Exception as e:
            if isinstance(e, InvalidCredentialsException):
                raise e
            raise InvalidCredentialsException("Erro ao alterar a senha.")

