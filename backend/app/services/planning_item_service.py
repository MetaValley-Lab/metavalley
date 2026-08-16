from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, cast

from app.core.supabase import supabase
from app.schemas.planning_item_schema import PlanningItemCreate, PlanningItemUpdate
from app.services.startup_service import StartupService

startup_service = StartupService()


class PlanningItemService:

    async def create_item(self, user_id: str, payload: PlanningItemCreate) -> Dict[str, Any]:
        startup = await startup_service.get_startup_by_id(str(payload.startup_id), user_id)
        if not startup:
            raise Exception("Startup não encontrada ou você não tem permissão.")

        data = payload.model_dump(mode="json")
        # A pessoa que criou é também quem fez a última atualização inicial
        data["last_updated_by"] = data["created_by"]

        response = supabase.table("planning_items").insert(data).execute()
        
        if not response.data:
            raise Exception("Erro ao criar planning item.")
        return cast(Dict[str, Any], response.data[0])

    async def get_items_by_startup(self, startup_id: str, user_id: str) -> List[Dict[str, Any]]:
        startup = await startup_service.get_startup_by_id(startup_id, user_id)
        if not startup:
            return []

        response = (
            supabase.table("planning_items")
            .select("*")
            .eq("startup_id", startup_id)
            .order("created_at", desc=False)
            .execute()
        )
        return cast(List[Dict[str, Any]], response.data or [])

    async def get_item_by_id(self, item_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("planning_items")
            .select("*, startups!inner(user_id)")
            .eq("id", item_id)
            .eq("startups.user_id", user_id)
            .execute()
        )
        if not response.data:
            return None
            
        item = cast(Dict[str, Any], response.data[0])
        item.pop("startups", None)
        return cast(Dict[str, Any], item)

    async def update_item(
        self, item_id: str, user_id: str, payload: PlanningItemUpdate
    ) -> Optional[Dict[str, Any]]:
        existing_item = await self.get_item_by_id(item_id, user_id)
        if not existing_item:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        
        # Mapeia quem atualizou para o banco de dados
        if "updated_by" in update_data:
            update_data["last_updated_by"] = update_data.pop("updated_by")

        # Gerencia data de conclusão
        if "completed" in update_data:
            if update_data["completed"] and not existing_item.get("completed"):
                update_data["completed_at"] = datetime.now(timezone.utc).isoformat()
            elif not update_data["completed"]:
                update_data["completed_at"] = None

        # Se só tinha o 'updated_by' e o 'completed_at' na requisição e mais nada mudou 
        # (ex: chamou update mas enviou os mesmos dados)
        if not update_data:
            return existing_item

        response = supabase.table("planning_items").update(update_data).eq("id", item_id).execute()
        return cast(Dict[str, Any], response.data[0]) if response.data else None

    async def delete_item(self, item_id: str, user_id: str) -> bool:
        existing_item = await self.get_item_by_id(item_id, user_id)
        if not existing_item:
            return False

        response = supabase.table("planning_items").delete().eq("id", item_id).execute()
        return isinstance(response.data, list) and len(response.data) > 0