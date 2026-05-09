from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session #essa função é um gerador, ela vai criar uma sessão, entregar ela para a função que chamou e depois de usar ela, ela vai fechar a sessão
    finally:
        session.close()