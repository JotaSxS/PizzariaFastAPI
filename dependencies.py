from models import Usuario, db
from sqlalchemy.orm import Session, sessionmaker, session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_scheme

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session #essa função é um gerador, ela vai criar uma sessão, entregar ela para a função que chamou e depois de usar ela, ela vai fechar a sessão
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    try:

        dic_info = jwt.decode(token, SECRET_KEY,ALGORITHM)
        id_usuario = int(dic_info.get("sub"))

    except JWTError:
        raise HTTPException(status_code=401, detail="Token de autenticação inválido ou expirado")
    
    usuario = session.query(Usuario).filter(Usuario.id==dic_info["sub"]).first()
    
    if not usuario:
    
        raise HTTPException(status_code=401, detail="Usuario não encontrado")
    
    return usuario