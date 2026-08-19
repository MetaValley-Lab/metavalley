from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SimulationInterestCreate(BaseModel):
    startup_id: UUID


class SimulationInterestResponse(BaseModel):
    id: UUID
    user_id: UUID
    startup_id: UUID
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    
class SimulationInterestStatusResponse(BaseModel):
    interested: bool
    
