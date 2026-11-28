"""
"Por que a pilha de desfazer não vive dentro da classe Playlist?"

    Porque as funcinalidades do desfazer não serião esclusivas da playlist, ela precisa ser usada em outra classe (essa) 
    pra englobar todas as funcionalidades da classe main e nao só as da playliste


"Por que a pilha (LIFO) é a estrutura certa para “desfazer”, e não uma lista comum?
O que aconteceria se você tentasse desfazer duas vezes seguidas sem fazer nenhuma
operação nova entre elas?"

    (Vou presumir que vc esteja se referindo a fifo quando se refere a "lista comun") a pilha LIFO é a certa pois a logica de "desfazer" 
    consiste em reverter a ultima ação feita, não a primeira que entrou na lista. 
    O certo (ou mais intuitivo) de que quando vc tentasse desfazer duas vezses seguidas, sem fazer nada entre as duas, seria que o programa "andasse para tras" 
    revertendo toas as ações feitas pelo usuario, como se todas interações fossem registradas e o "desfazer" fizesse a ação contraria, até o programa voltar 
    ao estado que estava antes de qualquer interação. Mas isso não seria possivel pois a estrutura da pilha lifo, só tem como ter acesso ao topo dela, ou seja,
    somente a ultima ação seria desfeita.
"""

from soundlab.acervo import Acervo
from soundlab.arvore import ArvoreBinaria
from soundlab.arvore_busca import ArvoreBusca
from soundlab.comparacao import comparar, montar_tabela
from soundlab.faixa import Faixa
from soundlab.fila import FilaCircular, FilaExecucao, trocar_modo
from soundlab.grafo import GrafoRecomendacao
from soundlab.pilha import Pilha
from soundlab.playlist import Playlist

OPCOES = """
+------------------- SoundLab -------------------+
1  Listar acervo           7  Inserir na playlist (posicao)
2  Cadastrar faixa         8  Tirar da playlist (posicao)
3  Buscar por titulo       9  Comecar reproducao (playlist)
4  Remover do acervo      10  Proxima faixa da playlist (>>)
5  Ver playlist           11  Faixa anterior da playlist (<<)
6  Acrescentar a playlist
                        12  Tocar faixa do acervo (historico)
                        13  Desfazer reproducao (historico)
                        14 Desfazer ultima interacao (playlist) (nova funcionalidade)
                        15 Adicionar a fila (a seguir)
                        16 Tocar proxima da fila
                        17 Ligar/desligar modo repeticao
                        18 Ver fila
                        19 Indice em arvore (3 percursos)
                        20 Buscar por titulo (arvore de busca)
                        21 Listar acervo em ordem alfabetica
                        22 Recomendar a partir de uma faixa
                        23 Comparar busca linear e binaria
0  Sair
+------------------------------------------------+"""


def carregar_acervo():
    acervo = Acervo()
    acervo.adicionar(Faixa("Aquarela do Brasil", "Ary Barroso", 245))
    acervo.adicionar(Faixa("Construcao", "Chico Buarque", 382))
    acervo.adicionar(Faixa("Ponta de Areia", "Milton Nascimento", 194))
    acervo.adicionar(Faixa("Baiao", "Luiz Gonzaga", 168))
    return acervo


def listar(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
    for posicao, faixa in enumerate(acervo):
        print(f"  [{posicao}] {faixa}")


def cadastrar(acervo):
    titulo = input("  titulo...: ").strip()
    artista = input("  artista..: ").strip()
    acervo.adicionar(Faixa(titulo, artista, int(input("  duracao (s): "))))
    print(f"  cadastrada. o acervo tem {len(acervo)} faixas.")


def buscar(acervo):
    faixa = acervo.buscar(input("  titulo: ").strip())
    print(f"  {faixa}" if faixa else "  nao encontrada")


def remover(acervo):
    faixa = acervo.remover(input("  titulo: ").strip())
    print(f"  removida: {faixa}" if faixa else "  nao encontrada")


def ver_playlist(playlist):
    print(f"  playlist '{playlist.nome}' ({len(playlist)} faixas)")
    for posicao, faixa in enumerate(playlist):
        print(f"    {posicao}. {faixa}")


def acrescentar(acervo, playlist):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    playlist.adicionar(faixa)
    print(f"  '{faixa.titulo}' entrou no fim da playlist")

# estou mudando aqui 
def inserir(acervo, playlist, pilha_desfazer): 
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    posicao = int(input(f"  posicao (0 a {len(playlist)}): "))
    playlist.inserir_em(posicao, faixa)

    # pilha_desfazer vai armazenar o tipo da ação para fazer o contrario depois e sua posição
    pilha_desfazer.empilhar((posicao, faixa, 'inserida'))

    print(f"  '{faixa.titulo}' inserida na posicao {posicao}")


def tirar(playlist, pilha_desfazer):
    posicao = int(input(f"  posicao (0 a {len(playlist) - 1}): "))

    # a mesmo caisa aconteçe aqui 
    faixa = playlist.remover_em(posicao)
    pilha_desfazer.empilhar((posicao, faixa, 'removida'))
    print(f"  saiu: {faixa}")


def comecar(playlist, grafo):
    faixa = playlist.comecar_reproducao()
    grafo.registrar_reproducao(faixa.titulo)
    print(f"  tocando: {faixa}")


def proxima(playlist, grafo):
    faixa = playlist.proxima()
    grafo.registrar_reproducao(faixa.titulo)
    print(f"  tocando: {faixa}")


def anterior(playlist, grafo):
    faixa = playlist.anterior()
    grafo.registrar_reproducao(faixa.titulo)
    print(f"  tocando: {faixa}")


def tocar_agora(acervo, historico, grafo):
    """Toca uma faixa direto do acervo, fora da ordem da playlist.

    Cada chamada empilha uma faixa nova: o topo do historico passa a
    ser "o que esta tocando agora".
    """
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    historico.empilhar(faixa)
    grafo.registrar_reproducao(faixa.titulo)
    print(f"  tocando agora: {faixa}")


def desfazer_reproducao(historico, grafo):
    """Desempilha a faixa atual e revela a que tocava antes dela —
    exatamente o oposto de tocar_agora."""
    if historico.vazia():
        print("  nada no historico")
        return
    atual = historico.desempilhar()
    print(f"  saindo de: {atual}")
    if historico.vazia():
        grafo.retomar_em(None)
        print("  historico vazio - nada tocando")
    else:
        grafo.retomar_em(historico.topo().titulo)
        print(f"  voltando a tocar: {historico.topo()}")

# A-aqui começa a função de desfazer a ultima interação
def desfazer_playlist(playlist, pilha_desfazer):

    # ve se a pilha esta vazia e volta
    if pilha_desfazer.vazia():
        print("nada para desfazer")
        return

    # começa a sua logica de desfazer a ultima ação e remove o topo da pilha
    posicao, faixa, acao = pilha_desfazer.desempilhar()

    # se a ação tiver sido inserir, remove a faixa
    if acao == 'inserida':
        playlist.remover_em(posicao)
        print(f"  desfazendo: '{faixa.titulo}' removida da posicao {posicao}")

    # e se a ação tiver sido remover, insere de novo
    elif acao == 'removida':
        playlist.inserir_em(posicao, faixa)
        print(f"  desfazendo: '{faixa.titulo}' inserida de volta na posicao {posicao}")


# Semana 1 - fila de execucao e modo repeticao
def enfileirar_faixa(acervo, fila):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    fila.enfileirar(faixa)
    print(f"  '{faixa.titulo}' entrou na fila")


def tocar_da_fila(fila, grafo):
    if fila.vazia():
        print("  fila vazia")
        return
    faixa = fila.desenfileirar()
    faixa.tocar()
    grafo.registrar_reproducao(faixa.titulo)
    print(f"  tocando: {faixa}")


def alternar_repeticao(fila):
    """Devolve a nova fila, que o main passa a usar."""
    nova = trocar_modo(fila)
    estado = "LIGADO" if isinstance(nova, FilaCircular) else "DESLIGADO"
    print(f"  modo repeticao {estado}")
    return nova


def ver_fila(fila):
    estado = "ligada" if isinstance(fila, FilaCircular) else "desligada"
    print(f"  a seguir ({len(fila)} faixas, repeticao {estado})")
    for posicao, faixa in enumerate(fila, start=1):
        print(f"    {posicao}. {faixa}")

# Semana 2 - arvore binaria como indice do acervo
def mostrar_percursos(acervo):
    """Monta a arvore com o acervo atual e mostra os tres percursos."""
    if len(acervo) == 0:
        print("  acervo vazio")
        return
    arvore = ArvoreBinaria()
    for faixa in acervo:
        arvore.inserir(faixa)

    pre = arvore.pre_ordem()
    em = arvore.em_ordem()
    pos = arvore.pos_ordem()

    largura = max(len("PRE-ORDEM"), max(len(faixa.titulo) for faixa in acervo))
    print(f"      {'PRE-ORDEM':<{largura}} | {'EM-ORDEM':<{largura}} | POS-ORDEM")
    for numero, (a, b, c) in enumerate(zip(pre, em, pos), start=1):
        print(f"  {numero:>2}. {a.titulo:<{largura}} | {b.titulo:<{largura}} | {c.titulo}")

# Semana 3 - arvore binaria de busca
def montar_abb(acervo):
    """Remontada a cada consulta, para refletir cadastros e remocoes."""
    arvore = ArvoreBusca()
    for faixa in acervo:
        arvore.inserir(faixa)
    return arvore


def buscar_na_abb(acervo):
    arvore = montar_abb(acervo)
    titulo = input("  titulo: ").strip()
    faixa = arvore.buscar(titulo)
    visitadas = arvore.caminho(titulo)
    if visitadas:
        print(f"  caminho: {' -> '.join(f.titulo for f in visitadas)}")
    print(f"  comparacoes: {len(visitadas)}")
    print(f"  {faixa}" if faixa else "  nao encontrada")


def listar_alfabetico(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
        return
    for faixa in montar_abb(acervo).em_ordem():
        print(f"  {faixa}")

# Semana 4 - recomendacao
def recomendar(acervo, grafo):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    todas = grafo.recomendar(faixa.titulo)
    if not todas:
        print("  ainda nao ha recomendacoes para essa faixa")
        return
    diretas = grafo.recomendar(faixa.titulo, 1)
    for titulo in todas:
        nivel = 1 if titulo in diretas else 2
        print(f"  {titulo} (distancia {nivel})")

#semmana 5
def comparar_buscas(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
        return
    print(f"  comparacoes feitas em um acervo de {len(acervo)} faixas")
    print(montar_tabela(comparar(acervo)))


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    historico = Pilha()

    # criando a pilha de desfazer as ações
    pilha_desfazer = Pilha()

    # fila "a seguir"; comeca com a repeticao desligada
    fila = FilaExecucao()

    grafo = GrafoRecomendacao()

    while True:
        print(OPCOES)
        opcao = input(" opcao: ").strip()
        try:
            if opcao == "0":
                print(" ate a proxima.")
                break
            elif opcao == "1": listar(acervo)
            elif opcao == "2": cadastrar(acervo)
            elif opcao == "3": buscar(acervo)
            elif opcao == "4": remover(acervo)
            elif opcao == "5": ver_playlist(playlist)
            elif opcao == "6": acrescentar(acervo, playlist)

            # agora essas obç~eos precisão passar a pilha para funcionar
            elif opcao == "7": inserir(acervo, playlist, pilha_desfazer)
            elif opcao == "8": tirar(playlist, pilha_desfazer)

            elif opcao == "9": comecar(playlist, grafo)
            elif opcao == "10": proxima(playlist, grafo)
            elif opcao == "11": anterior(playlist, grafo)
            elif opcao == "12": tocar_agora(acervo, historico, grafo)
            elif opcao == "13": desfazer_reproducao(historico, grafo)
            # a nova opççao
            elif opcao == "14": desfazer_playlist(playlist, pilha_desfazer)
            elif opcao == "15": enfileirar_faixa(acervo, fila)
            elif opcao == "16": tocar_da_fila(fila, grafo)
            elif opcao == "17": fila = alternar_repeticao(fila)
            elif opcao == "18": ver_fila(fila)
            elif opcao == "19": mostrar_percursos(acervo)
            elif opcao == "20": buscar_na_abb(acervo)
            elif opcao == "21": listar_alfabetico(acervo)
            elif opcao == "22": recomendar(acervo, grafo)
            elif opcao == "23": comparar_buscas(acervo)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()