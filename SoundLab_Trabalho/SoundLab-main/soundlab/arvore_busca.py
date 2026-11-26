"""É basicamente a arvore binaria da semana 2 so que agora tem uma regra de ordem em 
cada no, o titulo menor vai pra esquerda e o maior vai pra direita e ,se tiver titulo 
igual, vai pra direita tambem

Na pratica só a parte da inserção que muda mesmo. os tres percursos são herdados 
da arvore_binaria so que com essa regra nova, o em_ordem ja sai tudo em ordem 
alfabetica certinha

Os titulos são comparados usando o recurso lower() igual no Acervo.buscar pra letra 
maiuscula ou minuscula nao desordenar a ordem na hora de organizar
"""

from soundlab.arvore import ArvoreBinaria, NodoArvore

class ArvoreBusca(ArvoreBinaria):

    def inserir(self, faixa):

        novo = NodoArvore(faixa)

        if self._raiz is None:
            self._raiz = novo
            return

        chave = faixa.titulo.lower()
        nodo = self._raiz

        while True:
            if chave < nodo.faixa.titulo.lower():
                if nodo.esquerda is None:
                    nodo.esquerda = novo
                    return
                nodo = nodo.esquerda

            else:
                if nodo.direita is None:
                    nodo.direita = novo
                    return
                nodo = nodo.direita

    def buscar(self, titulo):
        chave = titulo.lower()

        for faixa in self._descer(chave):
            if faixa.titulo.lower() == chave:
                return faixa
        return None

    def caminho(self, titulo):
        return list(self._descer(titulo.lower()))

    def _descer(self, chave):
        nodo = self._raiz

        while nodo is not None:
            yield nodo.faixa
            atual = nodo.faixa.titulo.lower()
            if chave == atual:
                return
            nodo = nodo.esquerda if chave < atual else nodo.direita
