class Pessoa:
  def __init__(pessoa, nome, altura, time):
    pessoa.nome = nome
    pessoa.altura = altura
    pessoa.time = time

  def __str__(self):
    return f"nome:{self.nome}\ncpf:{self.altura}\nemail:{self.time}\n"