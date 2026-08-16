from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CanvasZoneKey(str, Enum):
    VALUE_PROPOSITION = "value_proposition"
    CUSTOMER_SEGMENTS = "customer_segments"
    ACQUISITION_CHANNELS = "acquisition_channels"
    REVENUE_MODEL = "revenue_model"
    COST_STRUCTURE = "cost_structure"
    KEY_RESOURCE = "key_resource"
    SUCCESS_METRICS = "success_metrics"


class CanvasZoneStatus(str, Enum):
    FILLED = "filled"
    IN_PROGRESS = "in_progress"
    TO_DEFINE = "to_define"


class ActorRole(str, Enum):
    FOUNDER = "founder"
    CEO = "ceo"
    CTO = "cto"
    CFO = "cfo"
    CMO = "cmo"


class CanvasZoneCreate(BaseModel):
    startup_id: UUID
    zone_key: CanvasZoneKey
    content: Optional[str] = None
    status: CanvasZoneStatus = CanvasZoneStatus.TO_DEFINE
    filled_by: ActorRole = Field(
        default=ActorRole.FOUNDER,
        description="Quem está preenchendo ou criando a zona do Canvas"
    )


class CanvasZoneUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[CanvasZoneStatus] = None
    filled_by: Optional[ActorRole] = Field(
        default=None,
        description="Quem está realizando a atualização da zona"
    )


class CanvasZoneResponse(BaseModel):
    id: UUID
    startup_id: UUID
    zone_key: CanvasZoneKey
    content: Optional[str] = None
    status: CanvasZoneStatus
    filled_by: ActorRole
    updated_at: datetime
    previous_content: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
