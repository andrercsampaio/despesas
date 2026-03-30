import sqlite3
from app.banco_de_dados.local import BancoDeDadosLocal
from app.modelos.usuarios import UsuarioResponse, UsuarioCriar

class UsuarioRepositorio:
    #receber a infraestrutura do banco de dados
    def __init__(self, db:BancoDeDadosLocal):
        self.db = db

    # def para criar e retornar um "usuário resposta"
    async def criar_usuarios (self, usuario: UsuarioCriar) -> UsuarioResponse:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome_usuario, nome_completo, email, senha)
                    VALUES (?, ?, ?, ?)
                    """, (usuario.nome_usuario, usuario.nome_completo, usuario.email, usuario.senha)
                )
                usuario_id = cursor.lastrowid
                dados_usuario = usuario.model_dump()
                return UsuarioResponse(id=usuario_id, **dados_usuario)
            except sqlite3.IntegrityError:
                raise Exception("nome de usuário ou e-mail já existente")
            
    #Lógica: atualizar usuario.
    async def atualizar_usuario(self, usuario_id: int, usuario: UsuarioCriar) -> UsuarioResponse | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute(
                    """
                    UPDATE usuarios 
                    SET nome_usuario = ?, nome_completo = ?, email = ?, senha = ?
                    WHERE id = ?
                    """,
                    (usuario.nome_usuario, usuario.nome_completo, usuario.email, usuario.senha, usuario_id)
                )
                
                if cursor.rowcount == 0:
                    return None
                    
                return UsuarioResponse(id=usuario_id, **usuario.model_dump())
            except sqlite3.IntegrityError:
                raise Exception("As novas credenciais (e-mail/usuário) já estão em uso.")


    #Lógica: deletar usuario.
    async def deletar_usuario(self, usuario_id: int) -> bool:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM usuarios WHERE id = ?", (usuario_id,)
            )
            return cursor.rowcount > 0
            

    #Lógica: Busca um usuário por email para validação ou login.        
    async def buscar_por_email(self, email: str) -> UsuarioResponse | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome_usuario, nome_completo, email FROM usuarios WHERE email = ?", 
                (email,)
            )
            linha = cursor.fetchone()
            
            if linha:
                return UsuarioResponse(
                    id=linha[0],
                    nome_usuario=linha[1],
                    nome_completo=linha[2],
                    email=linha[3]
                )
            return None
        
    #Lógica: Buscar um usuário por nome_usuario para validação ou login.   
    async def buscar_por_nome_usuario(self, nome_usuario: str) -> UsuarioResponse | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome_usuario, nome_completo, email FROM usuarios WHERE nome_usuario = ?", (nome_usuario,)
            )
            linha = cursor.fetchone()

            if linha: 
                return UsuarioResponse(
                    id=linha[0],
                    nome_usuario=linha[1],
                    nome_completo=linha[2],
                    email=linha[3]
                )
            return None