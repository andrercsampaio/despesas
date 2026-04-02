from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Importação das rotas
from app.rotas import usuarios_rotas, despesas_rotas, auth_web, despesas_web

# Importação do Middleware
from app.autenticacao_middleware import AuthenticationToken
from app.dependencias import banco_de_dados

app = FastAPI(title="Gestão de Despesas")

# 1. Pastas Estáticas e Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 2. Middleware de Cookies
app.add_middleware(AuthenticationToken)

# 3. Registro de Rotas
app.include_router(auth_web.router)       # Rota web de Login
app.include_router(despesas_web.router)
app.include_router(usuarios_rotas.router) # API JSON
app.include_router(despesas_rotas.router) # API JSON


@app.on_event("startup")
async def ao_iniciar():
    banco_de_dados.inicializar_banco()
    print("🚀 Servidor Web pronto!")

@app.get("/", response_class=HTMLResponse)
async def raiz(request: Request):
    # AJUSTE AQUI
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"titulo": "Dashboard de Despesas"}
    )