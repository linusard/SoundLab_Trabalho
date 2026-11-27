"""
grafo da semana 4

essa é a parte do ""quem escuyou X tmb ouviu Y". Cada música é um ponto e,quando 
duas músicas tocam uma depois da outra, a gente liga as elas.

"""

from soundlab.fila import FilaExecucao

class GrafoRecomendacao:

    def __init__(self):  
        self._adjacencia = {} 
        self._ultimo = None

    def registrar_coocorrencia(self, titulo_a, titulo_b):

        if titulo_a == titulo_b:
            return
        
        self._adjacencia.setdefault(titulo_a, set()).add(titulo_b)
        self._adjacencia.setdefault(titulo_b, set()).add(titulo_a)

    def registrar_reproducao(self, titulo):

        if self._ultimo is not None:
            self.registrar_coocorrencia(self._ultimo, titulo)
        self._ultimo = titulo

    def retomar_em(self, titulo):

        self._ultimo = titulo

    def recomendar(self, titulo, distancia_maxima=2):

        distancia = {titulo: 0}  
        fila = FilaExecucao()
        fila.enfileirar(titulo)
        recomendados = []

        while not fila.vazia():
            atual = fila.desenfileirar()

            if distancia[atual] >= distancia_maxima:
                continue
            for vizinho in self._adjacencia.get(atual, set()):
                if vizinho not in distancia:

                    # marca antes de enfileirar para não repetir em si msm
                    distancia[vizinho] = distancia[atual] + 1
                    fila.enfileirar(vizinho)
                    recomendados.append(vizinho)

        return recomendados
