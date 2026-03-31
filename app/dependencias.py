from typing import Annotated
from fastapi import Depends

from app.banco_de_dados.local import BancoDeDadosLocal
from app.banco_de_dados.despesas_repositorio import DespesasRepositorio
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio

# Instância única da infraestrutura (Singleton)
banco_de_dados = BancoDeDadosLocal()

#Fornece a instância única do banco de dados.
def obter_banco_de_dados() -> BancoDeDadosLocal:
    return banco_de_dados

#Injeta o banco no repositório de usuários e o fornece pronto para uso.
def obter_usuario_repositorio(
        banco_de_dados_local: Annotated[BancoDeDadosLocal, Depends(obter_banco_de_dados)]
    ) -> UsuarioRepositorio:
    return UsuarioRepositorio(banco_de_dados_local)

#Injeta o banco no repositório de despesas e o fornece pronto para uso.
def obter_despesas_repositorio(
        banco_de_dados_local: Annotated[BancoDeDadosLocal, Depends(obter_banco_de_dados)]
    ) -> DespesasRepositorio:
    return DespesasRepositorio(banco_de_dados_local)