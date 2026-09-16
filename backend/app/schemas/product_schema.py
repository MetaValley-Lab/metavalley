from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductType(str, Enum):
    SAAS = "saas"
    MARKETPLACE = "marketplace"
    APP = "app"
    HARDWARE = "hardware"
    SERVICE = "service"
    OTHER = "other"


class ProductStage(str, Enum):
    IDEA = "idea"
    PROTOTYPE = "prototype"
    MVP = "mvp"
    LAUNCHED = "launched"


class ProductActorRole(str, Enum):
    FOUNDER = "founder"
    CTO = "cto"


class ProductCreate(BaseModel):
    startup_id: UUID
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    type: ProductType
    price: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Preço atual ou pretendido"
    )
    stage: ProductStage = ProductStage.IDEA
    last_updated_by: ProductActorRole = ProductActorRole.FOUNDER


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    type: Optional[ProductType] = None
    price: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Preço atual ou pretendido"
    )
    stage: Optional[ProductStage] = None
    last_updated_by: Optional[ProductActorRole] = None


class ProductResponse(BaseModel):
    id: UUID
    startup_id: UUID
    name: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    type: ProductType
    price: Optional[Decimal] = None
    stage: ProductStage
    last_updated_by: ProductActorRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
