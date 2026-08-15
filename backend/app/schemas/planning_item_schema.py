from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ActorRole(str, Enum):
    FOUNDER = "founder"
    CEO = "ceo"
    CTO = "cto"
    CFO = "cfo"
    CMO = "cmo"


class PlanningItemCreate(BaseModel):
    startup_id: UUID
    content: str = Field(..., description="Descrição da tarefa ou próximo passo")
    created_by: ActorRole = Field(
        default=ActorRole.FOUNDER, 
        description="Quem está criando a tarefa (usuário ou IA)"
    )


class PlanningItemUpdate(BaseModel):
    content: Optional[str] = None
    completed: Optional[bool] = None
    updated_by: ActorRole = Field(
        default=ActorRole.FOUNDER, 
        description="Quem está atualizando a tarefa"
    )


class PlanningItemResponse(BaseModel):
    id: UUID
    startup_id: UUID
    content: str
    created_by: ActorRole
    last_updated_by: ActorRole
    completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)