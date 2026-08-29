import time

from filmes import carregar_filmes
from buscas import (
    busca_sequencial,
    busca_binaria,
    busca_interpolacao,
    montar_arvore_balanceada,
    TabelaHash,
)

CAMPOS = {
    "1": {
        "id": "codigo",
        "nome": "Código",
        "chave": lambda f: f.codigo,
        "conversor": int,
        "unico": True,
        "numerico": True,
    },
    "2": {
        "id": "titulo",
        "nome": "Título",
        "chave": lambda f: f.titulo.casefold(),
        "conversor": lambda texto: texto.casefold(),
        "unico": False,
        "numerico": False,
    },
    "3": {
        "id": "ano",
        "nome": "Ano",
        "chave": lambda f: f.ano,
        "conversor": int,
        "unico": False,
        "numerico": True,
    },
    "4": {
        "id": "genero",
        "nome": "Gênero",
        "chave": lambda f: f.genero.casefold(),
        "conversor": lambda texto: texto.casefold(),
        "unico": False,
        "numerico": False,
    },
}

METODOS = {
    "1": "Busca Sequencial",
    "2": "Busca Binária",
    "3": "Busca por Interpolação",
    "4": "Busca em Árvore Binária",
    "5": "Busca por Hashing",
}


def campos_disponiveis(metodo_id):
    if metodo_id == "3":
        return {k: v for k, v in CAMPOS.items() if v["numerico"]}
    return CAMPOS


def montar_estruturas(filmes):
    estruturas = {}
    for campo in CAMPOS.values():
        chave = campo["chave"]
        ordenados = sorted(filmes, key=chave)

        arvore = montar_arvore_balanceada(ordenados, chave=chave)

        tabela_hash = TabelaHash(tamanho=13, chave=chave)
        for filme in filmes:
            tabela_hash.inserir(filme)

        estruturas[campo["id"]] = {
            "ordenados": ordenados,
            "arvore": arvore,
            "hash": tabela_hash,
        }
    return estruturas


def executar_busca(metodo_id, campo, valor, filmes, estruturas):
    chave = campo["chave"]
    dados = estruturas[campo["id"]]

    if metodo_id == "1":
        return busca_sequencial(filmes, valor, chave=chave, chave_unica=campo["unico"])
    if metodo_id == "2":
        return busca_binaria(dados["ordenados"], valor, chave=chave)
    if metodo_id == "3":
        return busca_interpolacao(dados["ordenados"], valor, chave=chave)
    if metodo_id == "4":
        return dados["arvore"].buscar(valor)
    if metodo_id == "5":
        return dados["hash"].buscar(valor)
    raise ValueError(f"Método de busca desconhecido: {metodo_id}")


def listar_catalogo(filmes):
    print("\n--- Catálogo de filmes (ordenado por código) ---")
    for filme in sorted(filmes, key=lambda f: f.codigo):
        print(" ", filme)
    print()


def ler_valor_busca(campo):
    while True:
        entrada = input(f"{campo['nome']} (Enter para voltar): ").strip()
        if entrada == "":
            return None
        try:
            return campo["conversor"](entrada)
        except ValueError:
            print("Valor inválido para este campo.\n")


def buscar_no_submenu(metodo_id, metodo_nome, campo, filmes, estruturas):
    listar_catalogo(filmes)
    print(f"--- {metodo_nome} | Campo: {campo['nome']} ---")

    while True:
        valor = ler_valor_busca(campo)
        if valor is None:
            break

        inicio = time.perf_counter()
        encontrados, comparacoes = executar_busca(metodo_id, campo, valor, filmes, estruturas)
        fim = time.perf_counter()

        if encontrados:
            print(f"{len(encontrados)} filme(s) encontrado(s):")
            for filme in encontrados:
                print(" ", filme)
        else:
            print("Nenhum filme encontrado.")
        print(f"Comparações: {comparacoes} | Tempo: {(fim - inicio) * 1000:.4f} ms\n")


def menu_campo(metodo_id, metodo_nome, filmes, estruturas):
    campos = campos_disponiveis(metodo_id)

    while True:
        print(f"\n--- {metodo_nome}: buscar por qual campo? ---")
        for chave_menu, campo in campos.items():
            print(f"{chave_menu} - {campo['nome']}")
        print("0 - Voltar ao menu principal")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            return
        if escolha not in campos:
            print("Opção inválida!\n")
            continue

        buscar_no_submenu(metodo_id, metodo_nome, campos[escolha], filmes, estruturas)


def menu_principal():
    filmes = carregar_filmes()
    estruturas = montar_estruturas(filmes)

    while True:
        print("=================================================")
        print("   CATÁLOGO DE FILMES - MÉTODOS DE BUSCA (Cap. 5)")
        print("=================================================")
        for chave_menu, nome in METODOS.items():
            print(f"{chave_menu} - {nome}")
        print("6 - Listar catálogo")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Encerrando...")
            break
        elif escolha == "6":
            listar_catalogo(filmes)
        elif escolha in METODOS:
            menu_campo(escolha, METODOS[escolha], filmes, estruturas)
        else:
            print("Opção inválida!\n")


if __name__ == "__main__":
    menu_principal()
