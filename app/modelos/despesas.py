from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

class DespesaBase(BaseModel):
    descricao: str = Field(..., min_length=3, max_length=150)
    valor: float = Field(..., gt=0)
    categoria: Literal["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"]
    # Se o usuário não enviar, date.today() automaticamente
    data_despesa: date = Field(default_factory=date.today)

class DespesaCriar(DespesaBase):
    id_usuario: int # O ID do usuário que "dono" desta despesa

class DespesaResponse(DespesaBase):
    id: int
    id_usuario: int