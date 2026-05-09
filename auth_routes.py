from dependencies import pegar_sessao
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario,db
from sqlalchemy.orm import sessionmaker
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/autenticar", tags=["autenticação"])

@auth_router.get("/")
async def home():
    return {"mensagem" : "Voce acessou a rota de autenticacao", "autenticado":False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema , session: Session = Depends(pegar_sessao)):
    
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        #ja exite um usuario com esse email
        raise HTTPException(status_code=400, detail="Ja existe um usuario com esse email") 
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Conta criada com sucesso!{usuario_schema.email}"}    