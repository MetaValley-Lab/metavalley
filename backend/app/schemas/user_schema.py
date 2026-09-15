import phonenumbers
from phonenumbers import NumberParseException
from pydantic import BaseModel, field_validator
from typing import Optional

# 1. Função auxiliar reutilizável
def validar_telefone_aux(v: str | None) -> str | None:
    # Se o campo não foi enviado (é None), pula a validação e retorna None
    if v is None:
        return None
        
    try:
        parsed_number = phonenumbers.parse(v, "BR" if not v.startswith("+") else None)
        
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Número de telefone inválido.")
            
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        raise ValueError("Formato de número de telefone inválido.")


class UserEditProfileRequest(BaseModel):
    user_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    
    @field_validator("phone_number")
    @classmethod
    def validar_e_formatar_e164(cls, v: str | None) -> str | None:
        return validar_telefone_aux(v)
    
