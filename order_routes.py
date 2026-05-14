from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from sqlalchemy.orm import Session
from models import Pedido, Usuario, ItemPedido

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

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin :
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa operacao")
    else:
        pedidos = session.query(Pedido).all()
        return{
            "pedidos": pedidos
        }
    

@order_router.post("/pedido/adionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
   
   
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400,detail="Pedido nao existente")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401,detail="Voce nao tem autorizacao para realizar essa operacao")
    
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, item_pedido_schema.quantidade,id_pedido)

    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return{
        "mensagem"   : "Item criado com sucesso",
        "item_id"    : item_pedido.id,
        "preco_item" : pedido.preco
    }



