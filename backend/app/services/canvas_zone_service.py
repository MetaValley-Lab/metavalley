from typing import Any, Dict, List, Optional, cast

from app.core.supabase import supabase
from app.schemas.canvas_zone_schema import CanvasZoneCreate, CanvasZoneUpdate
from app.services.startup_service import StartupService


startup_service = StartupService()


class CanvasZoneService:

    async def create_zone(
        self,
        user_id: str,
        payload: CanvasZoneCreate
    ) -> Dict[str, Any]:
        startup = await startup_service.get_startup_by_id(
            str(payload.startup_id),
            user_id
        )

        if not startup:
            raise Exception("Startup não encontrada ou você não tem permissão.")

        data = payload.model_dump(mode="json")

        response = (
            supabase
            .table("canvas_zones")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise Exception("Erro ao criar Canvas Zone.")

        return cast(Dict[str, Any], response.data[0])

    async def get_zones_by_startup(
        self,
        startup_id: str,
        user_id: str
    ) -> List[Dict[str, Any]]:
        startup = await startup_service.get_startup_by_id(
            startup_id,
            user_id
        )

        if not startup:
            return []

        response = (
            supabase
            .table("canvas_zones")
            .select("*")
            .eq("startup_id", startup_id)
            .order("zone_key", desc=False)
            .execute()
        )

        return cast(List[Dict[str, Any]], response.data or [])

    async def get_zone_by_id(
        self,
        zone_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        response = (
            supabase
            .table("canvas_zones")
            .select("*, startups!inner(user_id)")
            .eq("id", zone_id)
            .eq("startups.user_id", user_id)
            .execute()
        )

        if not response.data:
            return None

        zone = cast(Dict[str, Any], response.data[0])
        zone.pop("startups", None)

        return zone

    async def update_zone(
        self,
        zone_id: str,
        user_id: str,
        payload: CanvasZoneUpdate
    ) -> Optional[Dict[str, Any]]:
        existing_zone = await self.get_zone_by_id(
            zone_id,
            user_id
        )

        if not existing_zone:
            return None

        update_data = payload.model_dump(
            exclude_unset=True,
            mode="json"
        )

        if not update_data:
            return existing_zone

        # Quando o conteúdo for alterado, preserva o conteúdo anterior.
        if "content" in update_data:
            new_content = update_data["content"]
            current_content = existing_zone.get("content")

            if new_content != current_content:
                update_data["previous_content"] = current_content

        response = (
            supabase
            .table("canvas_zones")
            .update(update_data)
            .eq("id", zone_id)
            .execute()
        )

        if not response.data:
            return None

        return cast(Dict[str, Any], response.data[0])

    async def delete_zone(
        self,
        zone_id: str,
        user_id: str
    ) -> bool:
        existing_zone = await self.get_zone_by_id(
            zone_id,
            user_id
        )

        if not existing_zone:
            return False

        response = (
            supabase
            .table("canvas_zones")
            .delete()
            .eq("id", zone_id)
            .execute()
        )

        return (
            isinstance(response.data, list)
            and len(response.data) > 0
        )