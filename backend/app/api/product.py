from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from supabase_auth import User
from supabase.client import Client

from app.api.dependencies import get_current_user
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService
from app.core.supabase import get_supabase_client


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)



@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    request: Request,
    payload: ProductCreate,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
        
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
        
    try:
        product_service = ProductService(supabase_client)
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
    request: Request,
    startup_id: UUID,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
        
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
        
    product_service = ProductService(supabase_client)
    return await product_service.get_products_by_startup(
        startup_id=str(startup_id),
        user_id=str(current_user.id)
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
async def get_product(
    request: Request,
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    product_service = ProductService(supabase_client)
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
    request: Request,
    product_id: UUID,
    payload: ProductUpdate,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    product_service = ProductService(supabase_client)
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


@router.post(
    "/{product_id}/image",
    response_model=ProductResponse
)
async def upload_product_image(
    request: Request,
    product_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    try:
        product_service = ProductService(supabase_client)
        product = await product_service.upload_product_image(
            product_id=str(product_id),
            user_id=str(current_user.id),
            file=file,
            supabase_client=supabase_client
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou acesso negado.",
        )
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    request: Request,
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
    else:
        token = request.cookies.get("access_token")

    if token:
        supabase_client.postgrest.auth(token)
    
    product_service = ProductService(supabase_client)
    deleted = await product_service.delete_product(
        product_id=str(product_id),
        user_id=str(current_user.id)
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou acesso negado."
        )
        
        
