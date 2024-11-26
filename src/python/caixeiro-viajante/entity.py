from random import random


class Cidade:
    def __init__(self, nome):
        self.nome = nome

class Individuo:
    def __init__(self, cidades, rotas, caminho, geracao=0, cromossomo=None):
        self.cidades = cidades
        self.rotas = rotas
        self.caminho = caminho
        self.geracao = geracao
        self.distancia_usada = 0
        self.cromossomo = cromossomo

        if cromossomo is None:
            self.gerar_cromossomo()

        self.nota_avaliacao = self.avaliacao()

    def gerar_cromossomo(self):
        self.cromossomo = []
        self.cromossomo.append(0)
        for i in range(len(self.rotas) - 2):
            ultimo_cromo = self.cromossomo[(i+1) - 1]
            #self.cromossomo.append(self._gerar_rota(ultimo_cromo))
            self.cromossomo.append(round((random() * (len(self.rotas) - 1))))
        self.cromossomo.append(0)

    def _gerar_rota(self, ultimo_cromo):
        lista_rotas = []

        for j in range(len(self.rotas)):
            if self.rotas[ultimo_cromo][j] != -1 and self.rotas[ultimo_cromo][j] != 0 and ultimo_cromo != j:
                lista_rotas.append(j)

        return lista_rotas[round((random() * (len(lista_rotas) - 1)))]

    def avaliacao(self):
        soma_distancia = 0
        roda_encontrada = []

        for i in range(len(self.cromossomo) - 1):
            distancia = self.rotas[self.cromossomo[i]][self.cromossomo[i+1]]
            if distancia == -1:
                soma_distancia += 500
            else:
                soma_distancia += distancia

            if self.cromossomo[i] in self.caminho and self.cromossomo[i] not in roda_encontrada:
                roda_encontrada.append(self.cromossomo[i])

        if len(roda_encontrada) != len(self.caminho):
            soma_distancia += 100 * (len(self.caminho) - len(roda_encontrada))

        return soma_distancia

    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))

        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte:len(self.cromossomo)]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte:len(self.cromossomo)]

        return [
            Individuo(self.cidades, self.rotas, self.caminho, self.geracao + 1, filho1),
            Individuo(self.cidades, self.rotas, self.caminho, self.geracao + 1, filho2)
        ]

    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao and i != 0 and i != len(self.cromossomo) - 1:
                self.cromossomo[i] = self._gerar_rota(self.cromossomo[i])

        self.nota_avaliacao = self.avaliacao()
        return self

    def cromossomo_to_view(self):
        cromossomoView = []
        for i in range(len(self.cromossomo)):
            cromossomoView.append(self.cidades[self.cromossomo[i]].nome)
        return cromossomoView

    def print(self):

        print(
            " ***** \n",
            "Geração: %s \n" % self.geracao,
            "Cromossomo: %s \n" % str(self.cromossomo_to_view()),
            "Avaliação: %s \n" % self.nota_avaliacao,
            "***** \n",
        )