class Pessoa:
    def __init__(self, nome, altura, time):
        self.nome = nome
        self.altura = altura
        self.time = time

    def __str__(self):
        return f"Nome: {self.nome}\nAltura: {self.altura}\nTime: {self.time}"
