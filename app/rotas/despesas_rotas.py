from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.modelos.despesas import DespesaCriar, DespesaResponse
from app.banco_de_dados.despesas_repositorio import DespesasRepositorio
from app.dependencias import obter_despesas_repositorio

router = APIRouter(prefix="/despesas", tags=["Despesas"])


#rota para criar despesas
@router.post("/criar/{usuario_id}", response_model=DespesaResponse, status_code=status.HTTP_201_CREATED)
async def criar_nova_despesa(
    usuario_id: int,
    despesa: DespesaCriar,
    repo: Annotated[DespesasRepositorio, Depends(obter_despesas_repositorio)]
) -> DespesaResponse:
    try:
        despesa.id_usuario = usuario_id
        return await repo.criar_despesa(despesa)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar despesa: {str(e)}"
        )
    
#rota para atualizar despesa
@router.put("/atualizar/{id_despesa}/{usuario_id}", response_model=DespesaResponse | None)
async def atualizar_despesa(
    usuario_id: int,
    id_despesa: int,
    despesa: DespesaCriar,
    repo: Annotated[DespesasRepositorio, Depends(obter_despesas_repositorio)]
) -> DespesaResponse:
    try:
        despesa.id_usuario = usuario_id
        despesa_atualizada = await repo.atualizar_despesa(id_despesa, despesa)
        return despesa_atualizada
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar despesa: {str(e)}"
        )
    
#rota para deletar despesa    
@router.delete("/deletar/{id_despesa}/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_despesa(
    id_despesa: int,
    usuario_id: int,
    repo: Annotated[DespesasRepositorio, Depends(obter_despesas_repositorio)]
):  
    despesa = await repo.obter_despesa(id_despesa)

    if despesa and despesa.id_usuario == usuario_id:
        sucesso = await repo.deletar_despesa(id_despesa)
        if sucesso:
            return 

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Despesa não encontrada!"
    )

#rota para listar todas despesas
@router.get("/{usuario_id}", response_model=list[DespesaResponse])
async def listar_despesas_usuario(
    usuario_id: int,
    repo: Annotated[DespesasRepositorio, Depends(obter_despesas_repositorio)],
    categoria: str | None = None, 
    data: date | None = None      
):
    return await repo.listar_despesas(usuario_id, categoria, data)