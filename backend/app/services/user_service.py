from supabase.client import Client
from app.core.exceptions import UserRegistrationException, UserEditException
from app.schemas.user_schema import UserEditProfileRequest
from app.services.image_service import upload_public_image
from fastapi import UploadFile, HTTPException, status # 👈 Adicionado para os tratamentos de erro

class UserService:
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    async def get_profile(self, user_id: str):
        response = (
            self.supabase.table("profiles")
            .select("id, username, phone_number, avatar_url")
            .eq("id", user_id)
            .execute()
        )
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil não encontrado."
            )
            
        # 🔥 RETORNO CORRIGIDO: Retorna o dicionário direto do Samir, tirando ele de dentro da lista []
        return response.data[0]


    
    async def complete_onboarding(self, user_id: str):
        try:
            response = (
                self.supabase.table("profiles")
                .update({"onboarding_completed": True})
                .eq("id", user_id)
                .execute()
            )
            
            return {
                "message": "Onboarding concluído com sucesso",
                "onboarding_completed": True
            }
            
        except Exception as e:
            raise UserRegistrationException(f"Erro ao atualizar o onboarding: {str(e)}")
        
        
    async def edit_profile(self, user_id: str, profile_edits: UserEditProfileRequest):
        payload = profile_edits.model_dump(exclude_unset=True)
        if "user_name" in payload:
            payload["username"] = payload.pop("user_name")
        
        if not payload:
            return {"message": "Nenhuma alteração foi fornecida."}
        
        try:
            response = (
                self.supabase.table("profiles")
                .update(payload)
                .eq("id", user_id)
                .execute()
            )
            
            return {
                "message": "Profile successfully edited"
            }
        except Exception as e:
            raise UserEditException(f"Erro ao atualizar as informações do perfil: {str(e)}")

    # 💡 Ajustado: Como a classe já possui 'self.supabase', não é necessário pedir o 'supabase_client' por parâmetro aqui.
    async def upload_avatar(self, user_id: str, file: UploadFile, supabase_client: Client):
        try:
            avatar_url = await upload_public_image(
                file=file,
                bucket="avatars",
                path=f"{user_id}/avatar",
                supabase_client=self.supabase # 👈 Usa o cliente injetado na classe
            )
            response = (
                self.supabase.table("profiles")
                .update({"avatar_url": avatar_url})
                .eq("id", user_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except ValueError:
            raise
        except Exception as e:
            raise UserEditException(f"Erro ao atualizar a foto de perfil: {str(e)}")
