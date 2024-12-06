from typing import Any

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    status: str | None
    message: str | None
    data: Any | None = None
    


class LoginSchema(BaseModel):
    email: str
    senha: str
    
    
class CategoriaSchema(BaseModel):
    nome: str


class FuncionarioSchema(BaseModel):
    id: int | None = None
    nome: str | None = None
    email: str | None = None
    senha: str | None = None
    telefone: str | None = None