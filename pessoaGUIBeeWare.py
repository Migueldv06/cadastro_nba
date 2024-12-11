import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from beeware.pessoaModelo import Pessoa
from beeware.pessoaPersistencia import PessoaPersistencia

class BeeWare(toga.App):
    pessoa = Pessoa(-1,"nome", 1, "@")

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "Nome: ",
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        altura_label = toga.Label(
            "Altura: ",
            style=Pack(padding=(0, 5))
        )
        self.altura_input = toga.TextInput(style=Pack(flex=1))

        time_label = toga.Label(
            "Time: ",
            style=Pack(padding=(0, 5))
        )
        self.email_input = toga.TextInput(style=Pack(flex=1))


        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        altura_box = toga.Box(style=Pack(direction=ROW, padding=5))
        altura_box.add(altura_label)
        altura_box.add(self.altura_input)

        time_box = toga.Box(style=Pack(direction=ROW, padding=5))
        time_box.add(time_label)
        time_box.add(self.time_input)

        button_cadastrar = toga.Button(
            "Cadastrar",
            on_press=self.instanciar,
            style=Pack(padding=5)
        )

        button_consultar = toga.Button(
            "Consultar",
            on_press=self.consultar,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(altura_box)
        main_box.add(time_box)
        main_box.add(button_cadastrar)
        main_box.add(button_consultar)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def instanciar(self, widget):
        pessoa = Pessoa(self.name_input.value, self.altura_input.value,
                                     self.time_input.value)
        print(pessoa)
        pessoaPersistencia = PessoaPersistencia(pessoa)
        pessoaPersistencia.inserir(pessoaPersistencia.pessoa)

    def consultar(self, widget):
        pessoa = Pessoa(-1, "nome", 1, "@")
        pessoaPersistencia = PessoaPersistencia(pessoa)
        pessoaPersistencia.consultar(pessoaPersistencia.pessoa)


def main():
    return BeeWare()