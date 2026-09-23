from typing import Any, Dict, List, Optional, cast

from app.core.supabase import supabase
from app.schemas.startup_schema import StartupCreate, StartupUpdate
from app.services.image_service import upload_public_image
from fastapi import UploadFile


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

    async def upload_startup_image(
        self, startup_id: str, user_id: str, file: UploadFile
    ) -> Optional[Dict[str, Any]]:
        startup = await self.get_startup_by_id(startup_id, user_id)
        if not startup:
            return None

        image_url = await upload_public_image(
            file=file,
            bucket="startup-images",
            path=f"{startup_id}/image",
        )
        response = (
            supabase.table("startups")
            .update({"image_url": image_url})
            .eq("id", startup_id)
            .eq("user_id", user_id)
            .execute()
        )
        return cast(Dict[str, Any], response.data[0]) if response.data else None

    async def delete_startup(self, startup_id: str, user_id: str) -> bool:
        response = (
            supabase.table("startups")
            .delete()
            .eq("id", startup_id)
            .eq("user_id", user_id)
            .execute()
        )
        return isinstance(response.data, list) and len(response.data) > 0