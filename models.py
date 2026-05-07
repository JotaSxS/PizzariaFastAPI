from  sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base 
from sqlalchemy_utils.types import ChoiceType

#cria a conexao com o banco de dados
db = create_engine("sqlite:///banco.db")

#cria a classe base para os modelos
Base = declarative_base()

#cria as tabelas/classes no banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self,nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"

   # STATUS_PEDIDOS = (
   #    ("PENDENTE", "Pendente"),
   #     ("CONCLUIDO", "Concluído"),
   #     ("CANCELADO", "Cancelado")
   # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    valor = Column("valor", Float)

    def __init__(self, usuario, status="PENDENTE", valor=0.0):
        self.usuario = usuario
        self.status = status
        self.valor = valor
    
    #  itens

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    pedido = Column("pedido", ForeignKey("pedidos.id"))
    nome_produto = Column("nome_produto", String)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    quantidade = Column("quantidade", Integer)
    preco_unitario = Column("preco_unitario", Float)

    def __init__(self, pedido, nome_produto, sabor, tamanho, quantidade, preco_unitario):

        self.pedido = pedido
        self.nome_produto = nome_produto
        self.sabor = sabor
        self.tamanho = tamanho
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario



#executa a criacao do metadados no banco de dados