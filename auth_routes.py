from dependencies import pegar_sessao
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario,db
from sqlalchemy.orm import sessionmaker
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/autenticar", tags=["autenticação"])

def criar_token(email):
    token = f"token_para_{email}"
    return token

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
    
# login -> email e senha -> verificar se o email existe no banco de dados -> se existir, comparar a senha digitada com a senha criptografada no banco de dados -> token de autenticação (JWT) -> resposta para o cliente com o token de autenticação
@auth_router.post("/login")
async def login(login_schema: LoginSchema , session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado")
    else: 
        acess_token = criar_token(usuario.email)
        return {
            "acess_token": acess_token,
            "token_type": "bearer"
        }