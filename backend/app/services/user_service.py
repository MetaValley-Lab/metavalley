from app.core.supabase import supabase
from app.core.exceptions import UserRegistrationException

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