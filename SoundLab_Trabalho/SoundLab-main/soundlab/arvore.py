"""

A estrutura não liniar: cada no guarda uma faixa e tem até duas outras faixas, que ficão um na
esquerda e outro a direita, funcionando como um indice para o acervo.

Sobre a regra de inserção: 
    ordem de chegada.
    a arvore é preenchida por "niveis", da esquerda para a direita.
    a posição não depende do título.

As três percursos são recursivos, visitam cada nó só uma vez e depois devolvem uma
lista des faixas
"""

from soundlab.fila import FilaExecucao


class NodoArvore:

    def __init__(self, faixa):
        self.faixa = faixa
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:

    def __init__(self):
        self._raiz = None

    def inserir(self, faixa):
        novo = NodoArvore(faixa)
        if self._raiz is None:
            self._raiz = novo
            return

        a_visitar = FilaExecucao()
        a_visitar.enfileirar(self._raiz)
        while not a_visitar.vazia():
            nodo = a_visitar.desenfileirar()
            if nodo.esquerda is None:
                nodo.esquerda = novo
                return
            if nodo.direita is None:
                nodo.direita = novo
                return
            a_visitar.enfileirar(nodo.esquerda)
            a_visitar.enfileirar(nodo.direita)

    def pre_ordem(self):
        """nó esquerda direita."""
        resultado = []
        self._pre_ordem(self._raiz, resultado)
        return resultado

    def _pre_ordem(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo.faixa)
        self._pre_ordem(nodo.esquerda, resultado)
        self._pre_ordem(nodo.direita, resultado)

    def em_ordem(self):
        """esquerda nó direita."""
        resultado = []
        self._em_ordem(self._raiz, resultado)
        return resultado

    def _em_ordem(self, nodo, resultado):
        if nodo is None:
            return
        self._em_ordem(nodo.esquerda, resultado)
        resultado.append(nodo.faixa)
        self._em_ordem(nodo.direita, resultado)

    def pos_ordem(self):
        """esquerda direita nó"""
        resultado = []
        self._pos_ordem(self._raiz, resultado)
        return resultado

    def _pos_ordem(self, nodo, resultado):
        if nodo is None:
            return
        self._pos_ordem(nodo.esquerda, resultado)
        self._pos_ordem(nodo.direita, resultado)
        resultado.append(nodo.faixa)
