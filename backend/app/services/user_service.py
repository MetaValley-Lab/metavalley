from app.core.supabase import supabase
from app.core.exceptions import UserRegistrationException, UserEditException
from app.schemas.user_schema import UserEditProfileRequest

class UserService:
    
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
        
