from app.core.supabase import supabase
from app.core.exceptions import UserRegistrationException, UserEditException
from app.schemas.user_schema import UserEditProfileRequest
from app.services.image_service import upload_public_image
from fastapi import UploadFile

class UserService:

    async def get_profile(self, user_id: str):
        response = (
            supabase.table("profiles")
            .select("id, username, phone_number, avatar_url")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return response.data
    
    async def complete_onboarding(self, user_id: str):
        try :
            response = (
                supabase.table("profiles")
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
                supabase.table("profiles")
                .update(payload)
                .eq("id", user_id)
                .execute()
            )
            
            return {
                "message": "Profile successfully edited"
            }
        except Exception as e:
            raise UserEditException(f"Erro ao atualizar as informações do perfil: {str(e)}")

    async def upload_avatar(self, user_id: str, file: UploadFile):
        try:
            avatar_url = await upload_public_image(
                file=file,
                bucket="avatars",
                path=f"{user_id}/avatar",
            )
            response = (
                supabase.table("profiles")
                .update({"avatar_url": avatar_url})
                .eq("id", user_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except ValueError:
            raise
        except Exception as e:
            raise UserEditException(f"Erro ao atualizar a foto de perfil: {str(e)}")
        
