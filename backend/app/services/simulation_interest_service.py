from typing import Any, Dict, List, Optional, cast

from app.core.supabase import supabase
from app.schemas.simulation_interest_schema import SimulationInterestCreate
from app.services.startup_service import StartupService


startup_service = StartupService()


class SimulationInterestService:

    async def create_interest(
        self,
        user_id: str,
        email: str,
        payload: SimulationInterestCreate
    ) -> Dict[str, Any]:
        startup = await startup_service.get_startup_by_id(
            str(payload.startup_id),
            user_id
        )

        if not startup:
            raise Exception(
                "Startup não encontrada ou você não tem permissão."
            )

        existing_interest = await self.get_user_interest(
            user_id=user_id,
            startup_id=str(payload.startup_id)
        )

        if existing_interest:
            raise Exception(
                "Você já demonstrou interesse nesta simulação."
            )

        data = {
            "user_id": user_id,
            "startup_id": str(payload.startup_id),
            "email": email,
        }

        response = (
            supabase
            .table("simulation_interests")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise Exception(
                "Erro ao registrar interesse na simulação."
            )

        return cast(Dict[str, Any], response.data[0])

    async def get_interests_by_startup(
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
            .table("simulation_interests")
            .select("*")
            .eq("startup_id", startup_id)
            .order("created_at", desc=False)
            .execute()
        )

        return cast(List[Dict[str, Any]], response.data or [])

    async def get_user_interest(
        self,
        user_id: str,
        startup_id: str
    ) -> Optional[Dict[str, Any]]:
        response = (
            supabase
            .table("simulation_interests")
            .select("*")
            .eq("user_id", user_id)
            .eq("startup_id", startup_id)
            .maybe_single()
            .execute()
        )
        
        data = response.data if response else None

        if not data:
            return None

        return cast(Dict[str, Any], data)

    async def has_user_interest(
        self,
        user_id: str,
        startup_id: str
    ) -> bool:
        interest = await self.get_user_interest(
            user_id=user_id,
            startup_id=startup_id
        )

        return interest is not None

    async def delete_interest(
        self,
        interest_id: str,
        user_id: str
    ) -> bool:
        response = (
            supabase
            .table("simulation_interests")
            .delete()
            .eq("id", interest_id)
            .eq("user_id", user_id)
            .execute()
        )

        deleted_data = response.data if response else None

        return (
            isinstance(deleted_data, list)
            and len(deleted_data) > 0
        )
        
