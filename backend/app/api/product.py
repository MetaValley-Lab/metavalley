from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from supabase_auth import User

from app.api.dependencies import get_current_user
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

product_service = ProductService()


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    payload: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        return await product_service.create_product(
            user_id=str(current_user.id),
            payload=payload
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get(
    "/startup/{startup_id}",
    response_model=List[ProductResponse]
)
async def get_startup_products(
    startup_id: UUID,
    current_user: User = Depends(get_current_user)
):
    return await product_service.get_products_by_startup(
        startup_id=str(startup_id),
        user_id=str(current_user.id)
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
async def get_product(
    product_id: UUID,
    current_user: User = Depends(get_current_user)
):
    product = await product_service.get_product_by_id(
        product_id=str(product_id),
        user_id=str(current_user.id)
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou acesso negado."
        )

    return product


@router.patch(
    "/{product_id}",
    response_model=ProductResponse
)
async def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    current_user: User = Depends(get_current_user)
):
    updated = await product_service.update_product(
        product_id=str(product_id),
        user_id=str(current_user.id),
        payload=payload
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou acesso negado."
        )

    return updated


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    product_id: UUID,
    current_user: User = Depends(get_current_user)
):
    deleted = await product_service.delete_product(
        product_id=str(product_id),
        user_id=str(current_user.id)
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou acesso negado."
        )
        
        
