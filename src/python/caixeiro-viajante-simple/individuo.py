from random import random

class Individuo:
    def __init__(self, cidades, rotas, caminho, centro_distribuicao, geracao=0, cromossomo=None):
        self.cidades = cidades
        self.rotas = rotas
        self.caminho = caminho
        self.centro_distribuicao = centro_distribuicao
        self.geracao = geracao
        self.distancia_percorrida = 0
        self.cidades_percorridas = 0
        self.cromossomo = cromossomo

        if cromossomo is None:
            self.gerar_cromossomo()

        self.nota_avaliacao = self.avaliacao()

    def gerar_cromossomo(self):
        caminho_aleatorio = []

        for i in range(len(self.rotas)):
            caminho_aleatorio.append(round((random() * (len(self.rotas) - 1))))

        self.cromossomo = caminho_aleatorio

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

        self.distancia_percorrida = soma_distancia
        self.cidades_percorridas = len(roda_encontrada)

        if len(roda_encontrada) != len(self.caminho):
            soma_distancia += 100 * (len(self.caminho) - len(roda_encontrada))

        if self.cromossomo[0] != self.centro_distribuicao:
            soma_distancia += 100

        if self.cromossomo[len(self.cromossomo) - 1] != self.centro_distribuicao:
            soma_distancia += 100

        return soma_distancia

    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))

        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte:len(self.cromossomo)]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte:len(self.cromossomo)]

        return [
            Individuo(self.cidades, self.rotas, self.caminho, self.centro_distribuicao, self.geracao + 1, filho1),
            Individuo(self.cidades, self.rotas, self.caminho, self.centro_distribuicao, self.geracao + 1, filho2)
        ]

    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                self.cromossomo[i] = round((random() * (len(self.rotas) - 1)))

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
            "Distância percorrida: %s \n" % self.distancia_percorrida,
            "Cidades percorridas: %s \n" % self.cidades_percorridas,
            "Avaliação: %s \n" % self.nota_avaliacao,
            "***** \n",
        )
