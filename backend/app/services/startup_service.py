from typing import Any, Dict, List, Optional, cast

from app.core.supabase import supabase
from app.schemas.startup_schema import StartupCreate, StartupUpdate


class StartupService:

    async def create_startup(self, user_id: str, payload: StartupCreate) -> Dict[str, Any]:
        data = payload.model_dump(exclude_unset=True)
        data["user_id"] = user_id

        response = supabase.table("startups").insert(data).execute()
        if not response.data:
            raise Exception("Erro ao cadastrar a startup.")
        
        return cast(Dict[str, Any], response.data[0])

    async def get_user_startups(self, user_id: str) -> List[Dict[str, Any]]:
        response = supabase.table("startups").select("*").eq("user_id", user_id).execute()
        return cast(List[Dict[str, Any]], response.data or [])

    async def get_startup_by_id(self, startup_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("startups")
            .select("*")
            .eq("id", startup_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data:
            return None
        
        return cast(Dict[str, Any], response.data[0])

    async def update_startup(
        self, startup_id: str, user_id: str, payload: StartupUpdate
    ) -> Optional[Dict[str, Any]]:
        update_data = payload.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_startup_by_id(startup_id, user_id)

        response = (
            supabase.table("startups")
            .update(update_data)
            .eq("id", startup_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data:
            return None
        
        return cast(Dict[str, Any], response.data[0])

    async def delete_startup(self, startup_id: str, user_id: str) -> bool:
        response = (
            supabase.table("startups")
            .delete()
            .eq("id", startup_id)
            .eq("user_id", user_id)
            .execute()
        )
        return isinstance(response.data, list) and len(response.data) > 0