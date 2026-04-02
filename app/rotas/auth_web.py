from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.dependencias import obter_usuario_repositorio
from app.modelos.usuarios import UsuarioCriar

router = APIRouter(tags=["Interface Web - Autenticação"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.post("/login")
async def processar_login(
    request: Request,
    repo: Annotated[UsuarioRepositorio, Depends(obter_usuario_repositorio)],
    email: str = Form(...),
    senha: str = Form(...)
):
    usuario = await repo.buscar_usuario_por_email_senha(email, senha)
    if usuario:
        # Redireciona para o painel de despesas após login
        response = RedirectResponse(url="/minhas-despesas", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)
        # O Pulo do Gato: Salvar o ID para buscar as despesas deste usuário depois
        response.set_cookie(key="usuario_id", value=str(usuario.id), httponly=True)
        return response
    
    return templates.TemplateResponse(
        request=request, name="login.html", context={"erro": "Credenciais inválidas."}
    )

@router.get("/registro", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request=request, name="registro.html")

@router.post("/registro")
async def processar_registro(
    request: Request,
    repo: Annotated[UsuarioRepositorio, Depends(obter_usuario_repositorio)],
    nome_usuario: str = Form(..., min_length=3),
    nome_completo: str = Form(..., min_length=3),
    email: str = Form(...),
    senha: str = Form(..., min_length=6)
):
    try:
        # A validação ocorre automaticamente ao instanciar o UsuarioCriar
        usuario_novo = UsuarioCriar(
            nome_usuario=nome_usuario, nome_completo=nome_completo, email=email, senha=senha
        )
        await repo.criar_usuarios(usuario_novo)
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            request=request, name="registro.html", context={"erro": str(e)}
        )

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session_token")
    response.delete_cookie("usuario_id")
    return response