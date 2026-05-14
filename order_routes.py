from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos",tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    return {"mensagem":"Voce acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso! Id do pedido: {novo_pedido.id}"}

@order_router.get("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # usuario.admin = true
    # usuario.id = pedido.usuario
    ### FAZER O MESMO PARA A CRIACAO DE PEDIDOS ###
    pedido = session.query(Pedido).filter(Pedido.id== id_pedido).first()
    if not pedido:
        raise HTTPException (status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException (status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    pedido.status = "CANCELADO"
    session.commit()
    return{
        # lazy-load apos o commit a sessao com o banco de dados e encerrada e temos que forcas o sistema a acessalo novamente pedido.id em vez de id_pedido
        "mensagem": f"Pedido numero: \" {pedido.id} \" cancelado com sucesso",
        "pedido"  : pedido
    }