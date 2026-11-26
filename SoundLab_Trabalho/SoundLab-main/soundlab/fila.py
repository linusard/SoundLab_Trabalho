"""
essa aki é a entrega da primeira semana (atrasada mas entregue). 
!!! eu nao conseui comitar na branch certa, por isso eu msm fiz o meu repertorio para fazer minhas entregas!!!!!!!

a fila funciona na logica FIFO (first in, first out), ou seja, o primeiro elemento que entra é o primeiro que sai. 
Na pratica tudo que entra vai por um lado (_tras) e tudo que sai vai pelo outro (_frente), parecido com uma fila comun 


aqui no SoundLab a fila foi usada pra fazer a lista "a seguir" (FilaExecucao), que vai tocando as musicas na ordem
que forão adicionadas. Ja a FilaCircular é uma variação da msma feita pro modo de repetição, onde o ultimo no aponta de volta 
pro primeiro, então quando chega no final ela recomeça do inicio sem para

sobre desempenho, tanto o enfileirar quanto o desenfileirar custão O(1), porque a gente meche direto nas 
pontas (_frente e _tras) usando os ponteiros, sem precisar ficar percorrendo a fila inteira toda vez que adciona ou tira
alguma coisa
"""


class No:
    """Um elo da fila: guarda um valor e aponta para o próximo nó."""

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class FilaExecucao:
    """Fila de reprodução (FIFO): a próxima faixa a tocar
    é sempre a que está há mais tempo esperando."""

    def __init__(self):
        self._frente = None
        self._tras = None
        self._tamanho = 0

    def enfileirar(self, faixa):
        """Insere no fim da fila. O(1)."""
        novo = No(faixa)
        if self.vazia():
            self._frente = novo
        else:
            self._tras.proximo = novo
        self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):
        """Remove e devolve a faixa da frente. O(1)."""
        if self.vazia():
            raise IndexError("fila vazia")
        no = self._frente
        self._frente = no.proximo
        if self._frente is None:
            # saiu o único nó: _tras não pode continuar apontando para ele
            self._tras = None
        self._tamanho -= 1
        return no.valor

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        """Percorre da frente para trás sem remover nada. Conta pelo
        tamanho porque na fila circular não existe um None no final."""
        no = self._frente
        for _ in range(self._tamanho):
            yield no.valor
            no = no.proximo


class FilaCircular(FilaExecucao):
    """Modo repetição: _tras.proximo aponta sempre para _frente.
    Quem é tocado não sai da fila, apenas passa para o fim."""

    def enfileirar(self, faixa):
        """Insere no fim e fecha o círculo de novo. O(1)."""
        super().enfileirar(faixa)
        self._tras.proximo = self._frente

    def desenfileirar(self):
        """Devolve a faixa da frente e gira o círculo uma posição:
        o nó tocado vira o _tras. Nenhum nó é criado ou apagado. O(1)."""
        if self.vazia():
            raise IndexError("fila vazia")
        self._tras = self._frente
        self._frente = self._frente.proximo
        return self._tras.valor


def trocar_modo(fila):
    """Liga ou desliga a repetição: devolve uma fila do outro tipo com as
    mesmas faixas, na mesma ordem. A fila recebida não deve mais ser usada.

    Custa O(n), mas só acontece na troca de modo. O laço é contado pelo
    tamanho, pois uma fila circular nunca fica vazia ao desenfileirar.
    """
    if isinstance(fila, FilaCircular):
        nova = FilaExecucao()
    else:
        nova = FilaCircular()
    for _ in range(len(fila)):
        nova.enfileirar(fila.desenfileirar())
    return nova