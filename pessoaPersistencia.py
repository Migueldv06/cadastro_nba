import mysql.connector
from beeware.pessoaModelo import Pessoa


class PessoaPersistencia:
    def __init__(self, pessoa):
        self.pessoa = pessoa

    def conexao(self):
        """Estabelece uma conexão com o banco de dados."""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            database="db_nba"
        )

    def inserir(self, jogador):
        """Insere um jogador na tabela 'jogador'."""
        try:
            conn = self.conexao()
            meuCursor = conn.cursor()
            sql = "INSERT INTO jogador (nome, altura, time) VALUES (%s, %s, %s)"
            valores = (jogador.nome, jogador.altura, jogador.time)
            meuCursor.execute(sql, valores)
            conn.commit()
            print(f"{meuCursor.rowcount} registro(s) inserido(s).")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir jogador: {err}")
        finally:
            meuCursor.close()
            conn.close()

    def consultar(self):
        """Consulta todos os jogadores na tabela 'jogador'."""
        try:
            conn = self.conexao()
            meuCursor = conn.cursor()
            sql = "SELECT jogador.id, jogador.nome, jogador.altura, time.cidade FROM jogador JOIN time ON jogador.time = time.id"
            meuCursor.execute(sql)
            resultados = meuCursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"Erro ao consultar jogadores: {err}")
            return []
        finally:
            meuCursor.close()
            conn.close()