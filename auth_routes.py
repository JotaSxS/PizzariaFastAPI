from fastapi import APIRouter

auth_router = APIRouter(prefix="/autenticar", tags=["autenticação"])

@auth_router.get("/")
async def autenticar():
    return {"mensagem" : "Voce acessou a rota de autenticacao", "autenticado":False}
