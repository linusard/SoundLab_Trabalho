# pra testar: python -m soundlab.comparacao
"""
A binária sempre ganha?
    pra achar aquarela por exemplo, a linear faz 1 comparaçao e a binaria faz 2

Por que o tamanho importa?
    paucas faixas = a diferença é pequena. muitas faixas = a vantagem 
    no pior caso aumenta conforme o acervo cresce

Por que ordenar?
    usa a ordem para não contar metade das comprarações ma binaria. A desordenada
    não não conseque usar esse recurso

A contagem inclui montar a árvore?
    não, ela só conta os itens examinados em cada bbusca
"""

import random

from soundlab.arvore_busca import ArvoreBusca
from soundlab.busca import busca_binaria_contada, busca_linear_contada
from soundlab.faixa import Faixa

INEXISTENTE = "Garota de Ipanema"


def lista_em_ordem(faixas):
    arvore = ArvoreBusca()

    for faixa in faixas:
        arvore.inserir(faixa)
    return arvore.em_ordem()


def escolher_titulos(faixas):
    total = len(faixas)

    if total <= 4:
        titulos = [faixa.titulo for faixa in faixas]

    else:
        posicoes = [0, total // 3, 2 * total // 3, total - 1]
        titulos = [faixas[posicao].titulo for posicao in posicoes]

    existentes = {faixa.titulo.lower() for faixa in faixas}
    ausentes = [t for t in (INEXISTENTE, "Asa Branca", "Wave", "Trem das Onze",
"Carinhoso", "Sampa", "Travessia", "Luar do Sertao","Tico-Tico no Fuba",
"Chega de Saudade")
                if t.lower() not in existentes]

    titulos.append(ausentes.pop(0))

    while len(titulos) < 5 and ausentes:
        titulos.append(ausentes.pop(0))
    return titulos


def comparar(faixas):

    faixas = list(faixas)
    ordenada = lista_em_ordem(faixas)
    linhas = []

    for titulo in escolher_titulos(faixas):
        achada, linear = busca_linear_contada(faixas, titulo)
        _, binaria = busca_binaria_contada(ordenada, titulo)
        linhas.append((titulo, achada is not None, linear, binaria))
    return linhas


def montar_tabela(linhas):

    largura = max(len("TITULO"), max(len(linha[0]) for linha in linhas))
    texto = [f"  {'TITULO':<{largura}} | ACHOU | LINEAR | BINARIA"]

    for titulo, achou, linear, binaria in linhas:
        resposta = "sim" if achou else "nao"
        texto.append(f"  {titulo:<{largura}} | {resposta:<5} | {linear:>6} | {binaria:>7}")
    media_linear = sum(linha[2] for linha in linhas) / len(linhas)
    media_binaria = sum(linha[3] for linha in linhas) / len(linhas)
    texto.append(f"  {'MEDIA':<{largura}} |       | {media_linear:>6.1f} | {media_binaria:>7.1f}")
    return "\n".join(texto)


def teste_com_100():

    faixas = [Faixa(f"Faixa {numero:03d}", "teste", 180) for numero in range(1, 101)]

    random.Random(1).shuffle(faixas)

    ordenada = lista_em_ordem(faixas)
    linear = [busca_linear_contada(faixas, f.titulo)[1] for f in faixas]
    binaria = [busca_binaria_contada(ordenada, f.titulo)[1] for f in faixas]

    return (f"  linear : media {sum(linear) / 100:.1f}, pior caso {max(linear)}\n"
            f"  binaria: media {sum(binaria) / 100:.1f}, pior caso {max(binaria)}")


if __name__ == "__main__":
    print("teste com 100 faixas de mentira (buscando cada uma):")
    print(teste_com_100())