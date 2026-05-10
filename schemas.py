from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] 
    admin: Optional[bool]

    class Config:
        from_atributes = True

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_atributes = True # Permite criar um schema a partir de um objeto ORM, ou seja, a partir de uma classe do SQLAlchemy.

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_atributes = True