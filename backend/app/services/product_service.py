from typing import Any, Dict, List, Optional, cast

from app.core.supabase import supabase
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.startup_service import StartupService
from app.services.image_service import upload_public_image
from fastapi import UploadFile


startup_service = StartupService()


class ProductService:

    async def create_product(
        self,
        user_id: str,
        payload: ProductCreate
    ) -> Dict[str, Any]:
        startup = await startup_service.get_startup_by_id(
            str(payload.startup_id),
            user_id
        )

        if not startup:
            raise Exception(
                "Startup não encontrada ou você não tem permissão."
            )

        data = payload.model_dump(
            mode="json",
            exclude_unset=True
        )

        response = (
            supabase
            .table("products")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise Exception("Erro ao criar produto.")

        return cast(
            Dict[str, Any],
            response.data[0]
        )

    async def get_products_by_startup(
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
            .table("products")
            .select("*")
            .eq("startup_id", startup_id)
            .order("created_at", desc=False)
            .execute()
        )

        return cast(
            List[Dict[str, Any]],
            response.data or []
        )

    async def get_product_by_id(
        self,
        product_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        response = (
            supabase
            .table("products")
            .select("*, startups!inner(user_id)")
            .eq("id", product_id)
            .eq("startups.user_id", user_id)
            .execute()
        )

        if not response.data:
            return None

        product = cast(
            Dict[str, Any],
            response.data[0]
        )

        product.pop("startups", None)

        return product

    async def update_product(
        self,
        product_id: str,
        user_id: str,
        payload: ProductUpdate
    ) -> Optional[Dict[str, Any]]:
        existing_product = await self.get_product_by_id(
            product_id,
            user_id
        )

        if not existing_product:
            return None

        update_data = payload.model_dump(
            exclude_unset=True,
            mode="json"
        )

        if not update_data:
            return existing_product

        response = (
            supabase
            .table("products")
            .update(update_data)
            .eq("id", product_id)
            .execute()
        )

        if not response.data:
            return None

        return cast(
            Dict[str, Any],
            response.data[0]
        )

    async def upload_product_image(
        self, product_id: str, user_id: str, file: UploadFile
    ) -> Optional[Dict[str, Any]]:
        product = await self.get_product_by_id(product_id, user_id)
        if not product:
            return None

        image_url = await upload_public_image(
            file=file,
            bucket="product-images",
            path=f"{product_id}/image",
        )
        response = (
            supabase.table("products")
            .update({"image_url": image_url})
            .eq("id", product_id)
            .execute()
        )
        return cast(Dict[str, Any], response.data[0]) if response.data else None

    async def delete_product(
        self,
        product_id: str,
        user_id: str
    ) -> bool:
        existing_product = await self.get_product_by_id(
            product_id,
            user_id
        )

        if not existing_product:
            return False

        response = (
            supabase
            .table("products")
            .delete()
            .eq("id", product_id)
            .execute()
        )

        return (
            isinstance(response.data, list)
            and len(response.data) > 0
        )
        
