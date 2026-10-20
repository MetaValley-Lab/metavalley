import phonenumbers
from phonenumbers import NumberParseException
from pydantic import EmailStr, BaseModel, Field, field_validator, model_validator


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8, 
        description="Senha do usuário"
    )
    
    
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(
        min_length=8,
        description="A senha deve no mínimo ter 8 caracteres."
    )
    phone_number: str = Field(
        description="Telefone no formato nacional (11 99999-8888) ou internacional (+1 202 555 0123)",
        examples=["(11) 99999-8888", "+5511999998888", "+12025550123"]
    )

    @field_validator("phone_number")
    @classmethod
    def validar_e_formatar_e164(cls, v: str) -> str:
        try:
            # Tenta fazer o parse. Se não houver '+', assume Brasil ('BR') como país padrão
            parsed_number = phonenumbers.parse(v, "BR" if not v.startswith("+") else None)
            
            # Valida se o número é realmente existente e válido no país de origem
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Número de telefone inválido.")
            
            # Retorna no padrão internacional E.164 (Ex: "+5511999998888" ou "+12025550123")
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            
        except NumberParseException:
            raise ValueError("Formato de número de telefone inválido.")
        

class ForgotPassword(BaseModel):
    email: str
    

class ResetPasswordRequest(BaseModel):
    code: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    new_password: str = Field(
        min_length=8,
        description="A senha deve ter no mínimo 8 caracteres" 
    )

    @model_validator(mode="after")
    def validate_credentials(self) -> "ResetPasswordRequest":
        has_code = bool(self.code and self.code.strip())
        has_access_token = bool(self.access_token and self.access_token.strip())
        has_refresh_token = bool(self.refresh_token and self.refresh_token.strip())

        if has_code and not has_access_token and not has_refresh_token:
            return self
        if not has_code and has_access_token and has_refresh_token:
            return self

        raise ValueError(
            "Forneça um código de restauração ou o par de tokens completo."
        )


class ChangePasswordSchema(BaseModel):
    current_password: str = Field(
        min_length=8,
        description="A senha deve no mínimo ter 8 caracteres."
    )
    new_password: str = Field(
        min_length=8,
        description="A senha deve no mínimo ter 8 caracteres."
    )