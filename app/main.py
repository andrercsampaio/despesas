from fastapi import FastAPI

# import de rotas
from app.rotas import usuarios_rotas, despesas_rotas

# dependencias
from app.dependencias import banco_de_dados


#app
app = FastAPI(
    title="Sistema de Gestão de Despesas",
    version="1.0.0"
)

# Rotas
app.include_router(usuarios_rotas.router)
app.include_router(despesas_rotas.router)



@app.on_event("startup")
async def ao_iniciar():
    """Garante a criação das tabelas no SQLite ao subir o servidor."""
    banco_de_dados.inicializar_banco()
    print("🚀 Infraestrutura de banco de dados pronta.")

@app.get("/", tags=["Healthcheck"])
async def raiz():
    return {"status": "online", "docs": "/docs"}