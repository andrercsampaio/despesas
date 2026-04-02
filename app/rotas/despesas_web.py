from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.banco_de_dados.despesas_repositorio import DespesasRepositorio
from app.dependencias import obter_despesas_repositorio
from app.modelos.despesas import DespesaCriar

router = APIRouter(prefix="/minhas-despesas", tags=["Interface Web - Despesas"])
templates = Jinja2Templates(directory="app/templates")

def extrair_usuario_id(request: Request) -> int:
    """Função utilitária para capturar o ID do cookie injetado no login."""
    usuario_id = request.cookies.get("usuario_id")
    return int(usuario_id) if usuario_id else 0

@router.get("/", response_class=HTMLResponse)
async def listar_despesas(
    request: Request,
    repo: Annotated[DespesasRepositorio, Depends(obter_despesas_repositorio)]
):
    usuario_id = extrair_usuario_id(request)
    despesas = await repo.listar_despesas(usuario_id=usuario_id)
    return templates.TemplateResponse(
        request=request, name="despesas.html", context={"despesas": despesas}
    )

@router.get("/nova", response_class=HTMLResponse)
async def pagina_criar_despesa(request: Request):
    return templates.TemplateResponse(request=request, name="despesa_form.html")

@router.post("/nova")
async def processar_nova_despesa(
    request: Request,
    repo: Annotated[DespesasRepositorio, Depends(obter_despesas_repositorio)],
    descricao: str = Form(..., min_length=3),
    valor: float = Form(..., gt=0),
    categoria: str = Form(...)
):
    usuario_id = extrair_usuario_id(request)
    try:
        # A validação Pydantic garante a integridade dos dados inseridos no form
        nova_despesa = DespesaCriar(
            descricao=descricao, valor=valor, categoria=categoria, id_usuario=usuario_id
        )
        await repo.criar_despesa(nova_despesa)
        return RedirectResponse(url="/minhas-despesas", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            request=request, name="despesa_form.html", context={"erro": str(e)}
        )