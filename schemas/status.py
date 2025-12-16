from pydantic import BaseModel, Field

class MensagemSchema(BaseModel):
    message: str = Field(..., description="Mensagem de resposta")

class ErrorSchema(BaseModel):
    error: str = Field(..., description="Mensagem de erro")
