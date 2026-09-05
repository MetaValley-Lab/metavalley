from pydantic import BaseModel, ConfigDict
from uuid import UUID
from enum import Enum
from typing import Any, Optional
from datetime import datetime 

class MessageRequest(BaseModel):
    startup_id: UUID
    message: str
    mode: str = "casual"
    conversation_type: str = "group"
    # conversation_type aceita: "group" | "onboarding" | "ceo" | "cto" | "cfo" | "cmo"
    
    
class ConversationType(str, Enum):
    ONBOARDING = "onboarding"
    GROUP = "group"
    CEO = "ceo"
    CTO = "cto"
    CFO = "cfo"
    CMO = "cmo"
    
    
class MessageRole(str, Enum):
    USER = "user"
    AGENT = "agent"
 
 
class AgentName(str, Enum):
    FOUNDER = "founder"
    CEO = "ceo"
    CTO = "cto"
    CFO = "cfo"
    CMO = "cmo"


class ConversationResponse(BaseModel):
    id: UUID
    startup_id: UUID
    type: ConversationType
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: MessageRole
    agent_name: Optional[AgentName] = None  # NULL para mensagens do founder
    content: str
    actions: Optional[list[Any]] = None     # JSONB — auditoria das actions executadas
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)

    