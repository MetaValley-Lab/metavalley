from pydantic import BaseModel
from uuid import UUID

class MessageRequest(BaseModel):
    startup_id: UUID
    message: str
    mode: str = "casual"
    conversation_type: str = "group"
    # conversation_type aceita: "group" | "onboarding" | "ceo" | "cto" | "cfo" | "cmo"