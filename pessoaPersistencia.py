import mysql.connector
from beeware.pessoaModelo import Pessoa


class PessoaPersistencia:
    pessoaM = Pessoa(-1,"nome", 1, "@")

    def __init__(self, pessoa):
        self.pessoa = pessoa
        pessoaM = pessoa

    def conexao(self):
        global meuBancoDeDados
        meuBancoDeDados = mysql.connector.connect(
            host="localhost",#192.168.56.1:3306
            user="root",
            #password="yourpassword",#só coloque senha se for diferente de vazio
            database="db_nba"
        )

        meuCursor = meuBancoDeDados.cursor()
        return meuCursor

    def inserir(self, jogador):
        meuCursor = self.conexao()
        sql = "INSERT INTO jogador (nome, altura, tima) VALUES (%s, %s, %s)"
        valor = (jogador.nome, jogador.altura, jogador.time)
        meuCursor.execute(sql, valor)

        meuBancoDeDados.commit()
        print(meuCursor.rowcount, "registro inserido.")

    def consultar(self, pessoa):
        meuCursor = self.conexao()
        sql = "SELECT * FROM Pessoa"
        meuCursor.execute(sql)

        meusResultados = meuCursor.fetchall()

        listaPessoas = []
        for resultado in meusResultados:
            pessoa = Pessoa(resultado[0], resultado[1], resultado[2], resultado[3])
            listaPessoas.append(pessoa)
            print(resultado)
            print(resultado[0]," - ", resultado[1]," - ", resultado[2]," - ", resultado[3])

        return listaPessoas