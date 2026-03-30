import sqlite3
from app.banco_de_dados.local import BancoDeDadosLocal
from app.modelos.despesas import DespesaResponse, DespesaCriar


class DespesasRepositorio:
    #receber a infraestrutura do banco de dados
    def __init__(self, banco_de_dados: BancoDeDadosLocal):
        self.db = banco_de_dados
        
    # def para criar e retornar uma  "despesa resposta"
    async def criar_despesa(self, despesa: DespesaCriar) -> DespesaResponse:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                INSERT INTO despesas (id_usuario, descricao, valor, categoria, data_despesa) 
                VALUES (?, ?, ?, ?, ?)
                """, 
                (despesa.id_usuario, despesa.descricao, despesa.valor, despesa.categoria, str(despesa.data_despesa))
            )
            despesa_id = cursor.lastrowid
            return DespesaResponse(id=despesa_id, **despesa.model_dump())
        
    #Lógica: atualizar despesa.
    async def atualizar_despesa(self, despesa_id: int, despesa: DespesaCriar) -> DespesaResponse | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE despesas SET descricao = ?, valor = ?, categoria = ?, data_despesa= ? WHERE id = ?",
                (despesa.descricao, despesa.valor, despesa.categoria, despesa.data_despesa,  despesa_id)
            )
            if cursor.rowcount == 0:
                return None
            return DespesaResponse(id=despesa_id, **despesa.model_dump())

    #Lógica: deletar despesa.
    async def deletar_despesa(self, despesa_id: int) -> bool:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM despesas WHERE id = ?", (despesa_id,)
            )
            return cursor.rowcount > 0
        

    #Lógica: Listar despesas.
    async def listar_despesas(self) -> list[DespesaResponse]:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, id_usuario, descricao, valor, categoria, data_despesa FROM despesas")
            linhas = cursor.fetchall()
            return [
                DespesaResponse(
                    id=l[0], id_usuario=l[1], descricao=l[2], 
                    valor=l[3], categoria=l[4], data_despesa=l[5]
                ) for l in linhas
            ]
        
    #Lógica: Busca uma despesa. 
    async def obter_despesa(self, despesa_id: int) -> DespesaResponse | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, id_usuario, descricao, valor, categoria, data_despesa FROM despesas WHERE id = ?", (despesa_id,))
            linha = cursor.fetchone()
            if linha:
                return DespesaResponse(
                    id=linha[0], 
                    id_usuario=linha[1], 
                    descricao=linha[2], 
                    valor=linha[3], 
                    categoria=linha[4], 
                    data_despesa=linha[5]
                )
            return None