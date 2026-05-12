from dependencies import pegar_sessao, verificar_token
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario,db
from sqlalchemy.orm import sessionmaker
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/autenticar", tags=["autenticação"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info ={
        "sub": str(id_usuario),
        "exp": data_expiracao
    }

    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)

    #token = f"token_para_{id_usuario}"
    return jwt_codificado



def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False 
    return usuario

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
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado ou credenciais invalidas")
    else: 
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, timedelta(days=3))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
### login para o formulario OAuth2PasswordRequestForm
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado ou credenciais invalidas")
    else: 
        access_token = criar_token(usuario.id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    
@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
    
    access_token = criar_token(usuario.id)
    return{
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
    }