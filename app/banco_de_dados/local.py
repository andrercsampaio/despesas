#biblioteca para banco de dados
import sqlite3

"""
Decorador que permite transformar uma função em um "gerenciador de contexto". 
Isso permite que você use a função dentro de um bloco with,
 automatizando o setup (abrir conexão) e o teardown (fechar conexão).
"""
from contextlib import contextmanager

class BancoDeDadosLocal():
    def __init__(self, nome_arquivo='despesas.db'):
        self.nome_arquivo = nome_arquivo
        self.inicializar_banco()

    @contextmanager
    def conectar(self):
        # O parâmetro check_same_thread=False é obrigatório para rodar com FastAPI
        conexao = sqlite3.connect(self.nome_arquivo, check_same_thread=False)
        # Ativa explicitamente o suporte a chaves estrangeiras para esta conexão
        conexao.execute("PRAGMA foreign_keys = ON;")
        try:
            #'pausar'
            yield conexao
            #salvar
            conexao.commit()

        except Exception as e:
            #desfazer as alteração em casa de erro para não corromper os dados
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def inicializar_banco(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            # Tabela de Usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_usuario TEXT UNIQUE NOT NULL,
                    nome_completo TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL
                )
            ''')

            # Tabela de Despesas (Relacionada)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS despesas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    valor REAL NOT NULL,
                    categoria TEXT NOT NULL,
                    data_despesa TEXT NOT NULL, 
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
                )
            ''')
        
            # O PULO DO GATO: Criação de índices para busca rápida
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_despesas_usuario ON despesas(id_usuario)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)')

        print("Banco de dados inicializado")