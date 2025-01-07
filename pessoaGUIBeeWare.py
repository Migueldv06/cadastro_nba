import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from mysql.connector import connect

from beeware.pessoaModelo import Pessoa
from beeware.pessoaPersistencia import PessoaPersistencia


class BeeWare(toga.App):
    pessoa = Pessoa("nome", "altura", "time")

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        # Nome
        name_label = toga.Label("Nome: ", style=Pack(padding=(0, 5)))
        self.name_input = toga.TextInput(style=Pack(flex=1))

        # Altura
        altura_label = toga.Label("Altura: ", style=Pack(padding=(0, 5)))
        self.altura_input = toga.TextInput(style=Pack(flex=1))

        # Time
        time_label = toga.Label("Time: ", style=Pack(padding=(0, 5)))
        self.time_dropdown = toga.Selection(style=Pack(flex=1))

        # Carregar times no dropdown
        self.load_teams()

        # Layout dos campos
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        altura_box = toga.Box(style=Pack(direction=ROW, padding=5))
        altura_box.add(altura_label)
        altura_box.add(self.altura_input)

        time_box = toga.Box(style=Pack(direction=ROW, padding=5))
        time_box.add(time_label)
        time_box.add(self.time_dropdown)

        # Botões
        button_criar_time = toga.Button("Criar Time", on_press=self.criar_time, style=Pack(padding=5))
        button_cadastrar = toga.Button("Cadastrar", on_press=self.instanciar, style=Pack(padding=5))
        button_consultar = toga.Button("Consultar", on_press=self.consultar, style=Pack(padding=5))

        # Adicionando os componentes ao main_box
        main_box.add(name_box)
        main_box.add(altura_box)
        main_box.add(time_box)
        main_box.add(button_criar_time)
        main_box.add(button_cadastrar)
        main_box.add(button_consultar)

        # Configurando a janela principal
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def criar_time(self, widget):
        """Abre uma janela para cadastrar um novo time."""
        # Caixa principal para a janela
        create_team_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Campo para o nome do time
        team_name_label = toga.Label("Nome do Time:", style=Pack(padding=(0, 5)))
        self.team_name_input = toga.TextInput(style=Pack(flex=1))

        # Layout dos campos
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(team_name_label)
        name_box.add(self.team_name_input)

        # Botão para salvar o time
        save_button = toga.Button(
            "Salvar Time",
            on_press=self.salvar_time,
            style=Pack(padding=5)
        )

        # Adicionando os campos e botão à caixa principal
        create_team_box.add(name_box)
        create_team_box.add(save_button)

        # Janela para cadastro de time
        self.create_team_window = toga.Window(title="Cadastro de Time")
        self.create_team_window.content = create_team_box
        self.create_team_window.show()

    def salvar_time(self, widget):
        """Salva o novo time no banco de dados."""
        try:
            # Conexão com o banco
            connection = connect(
                host="localhost",
                user="root",
                database="db_nba"
            )
            cursor = connection.cursor()

            # Inserindo o time no banco
            sql = "INSERT INTO time (nome) VALUES (%s)"
            values = (self.team_name_input.value.strip(),)
            cursor.execute(sql, values)
            connection.commit()

            print(f"Time '{self.team_name_input.value}' adicionado com sucesso!")
            self.create_team_window.close()  # Fecha a janela após o cadastro
        except Exception as e:
            print(f"Erro ao salvar time: {e}")
        finally:
            cursor.close()
            connection.close()

    def load_teams(self):
        """Carrega os times disponíveis do banco de dados e popula o dropdown."""
        try:
            connection = connect(
                host="localhost",
                user="root",
                database="db_nba"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT id, nome FROM time")
            teams = cursor.fetchall()

            self.time_dropdown.items.clear()
            for team_id, team_name in teams:
                self.time_dropdown.items.append(f"{team_name} ({team_id})")

            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Erro ao carregar times: {e}")

    def instanciar(self, widget):
        """Registra um jogador no banco de dados."""
        try:
            if not self.time_dropdown.value:
                print("Nenhum time selecionado!")
                return

            # Extrai o ID do time da string selecionada
            selected_team_id = int(self.time_dropdown.value.split("(")[-1].rstrip(")"))

            # Cria o objeto Pessoa
            pessoa = Pessoa(
                self.name_input.value.strip(),
                float(self.altura_input.value.strip()),
                selected_team_id
            )

            # Persiste o jogador no banco de dados
            pessoaPersistencia = PessoaPersistencia(pessoa)
            pessoaPersistencia.inserir(pessoa)

            print(f"Jogador {pessoa.nome} inserido com sucesso!")
        except ValueError:
            print("Erro ao converter altura ou ID do time.")
        except Exception as e:
            print(f"Erro ao inserir jogador: {e}")

    def consultar(self, widget):
        """Consulta todos os jogadores no banco de dados e exibe na interface."""
        try:
            pessoaPersistencia = PessoaPersistencia(None)
            resultados = pessoaPersistencia.consultar()

            # Exibir resultados
            for resultado in resultados:
                print(f"ID: {resultado[0]}, Nome: {resultado[1]}, Altura: {resultado[2]}, Time: {resultado[3]}")
        except Exception as e:
            print(f"Erro ao consultar jogadores: {e}")


def main():
    return BeeWare()
