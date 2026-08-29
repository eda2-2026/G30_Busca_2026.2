import csv
import os

CAMINHO_CSV_PADRAO = os.path.join(os.path.dirname(__file__), "filmes.csv")


class Filme:
    def __init__(self, codigo, titulo, ano, genero):
        self.codigo = codigo
        self.titulo = titulo
        self.ano = ano
        self.genero = genero

    def __str__(self):
        return f"[{self.codigo:>5}] {self.titulo} ({self.ano}) - {self.genero}"


def carregar_filmes(caminho_csv=CAMINHO_CSV_PADRAO):
    filmes = []
    with open(caminho_csv, newline="", encoding="utf-8") as arquivo_csv:
        leitor = csv.DictReader(arquivo_csv)
        for linha in leitor:
            filmes.append(
                Filme(
                    codigo=int(linha["codigo"]),
                    titulo=linha["titulo"],
                    ano=int(linha["ano"]),
                    genero=linha["genero"],
                )
            )
    return filmes
