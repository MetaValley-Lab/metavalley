from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StartupStage(str, Enum):
    IDEA = "idea"
    MVP = "mvp"
    LAUNCHED = "launched"


class RevenueModel(str, Enum):
    SUBSCRIPTION = "subscription"
    SAAS = "saas"
    MARKETPLACE = "marketplace"
    FREEMIUM = "freemium"
    PAY_PER_USE = "pay_per_use"
    LICENSING = "licensing"
    ADVERTISING = "advertising"
    E_COMMERCE = "e_commerce"
    SERVICE = "service"
    HARDWARE = "hardware"
    OTHER = "other"


class StartupStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class StartupBase(BaseModel):
    name: str = Field(..., max_length=255, description="Nome da startup")
    description: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    segment: Optional[str] = Field(None, max_length=255)
    target_location: Optional[str] = Field(None, max_length=255)
    stage: StartupStage = StartupStage.IDEA
    primary_revenue_model: Optional[RevenueModel] = None
    revenue_model_details: Optional[str] = None
    status: StartupStatus = StartupStatus.ACTIVE


class StartupCreate(StartupBase):
    pass


class StartupUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    segment: Optional[str] = Field(None, max_length=255)
    target_location: Optional[str] = Field(None, max_length=255)
    stage: Optional[StartupStage] = None
    primary_revenue_model: Optional[RevenueModel] = None
    revenue_model_details: Optional[str] = None
    status: Optional[StartupStatus] = None


class StartupResponse(StartupBase):
    id: UUID
    user_id: UUID
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)