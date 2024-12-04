from random import random

from individuo import Individuo

class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, debug_mode = False):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.lista_solucoes = []
        self.melhor_solucao = None

        self.debug_mode = debug_mode

    def inicializa_populacao(self, cidades, rotas, caminho, centro_distribuicao):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(cidades, rotas, caminho, centro_distribuicao))
        self.melhor_solucao = self.populacao[0]

    def ordena_populacao(self):
        self.populacao = sorted(
            self.populacao,
            key=lambda individuo: individuo.nota_avaliacao,
            reverse=False
        )

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao < self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao

        return soma

    def visualiza_geracao(self):
        if not self.debug_mode:
            return

        print(
            " ***** \n",
            "Geração: %s \n" % self.populacao[0].geracao,
            "Melhor solução: %s \n" % self.populacao[0].nota_avaliacao,
            "Melhor distância percorrida: %s \n" % self.populacao[0].distancia_percorrida,
            "Melhor total de cidades percorridas: %s \n" % self.populacao[0].cidades_percorridas,
            "Melhor Cromossomo: %s \n" % str(self.populacao[0].cromossomo_to_view()),
            "***** \n",
        )

    def visualiza_melhor_geracao(self):
        if not self.debug_mode:
            return

        print(
            " ***** (Melhor solução) ***** \n",
            "Geração: %s \n" % self.melhor_solucao.geracao,
            "Melhor solução: %s \n" % self.melhor_solucao.nota_avaliacao,
            "Melhor distância percorrida: %s \n" % self.melhor_solucao.distancia_percorrida,
            "Melhor total de cidades percorridas: %s \n" % self.melhor_solucao.cidades_percorridas,
            "Melhor Cromossomo: %s \n" % str(self.melhor_solucao.cromossomo_to_view()),
            "***** ================ *****\n",
        )

    def gerar_probabilidade(self):
        pesos = []

        for i in range(len(self.populacao)):
            pesos.append(1 / (i+1))

        soma_pesos = sum(pesos)

        for j in range(len(self.populacao)):
            self.populacao[j].probabilidade =  (pesos[j] / soma_pesos) * 100

    def seleciona_pai(self):
        cumulativas = []
        soma = 0
        for i in range(self.tamanho_populacao):
            soma += self.populacao[i].probabilidade
            cumulativas.append(soma)

        numero_aleatorio = round(random() * 100)

        for i, limite in enumerate(cumulativas):
            if numero_aleatorio < limite:
                return i
        return self.seleciona_pai()

    def resolver(self, taxa_mutacao, numero_geracoes, cidades, rotas, caminho, centro_distribuicao):
        self.inicializa_populacao(cidades, rotas, caminho, centro_distribuicao),
        self.ordena_populacao()
        self.gerar_probabilidade()
        self.visualiza_geracao()
        self.lista_solucoes.append(self.populacao[0].nota_avaliacao)

        for i in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []

            for j in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai()
                pai2 = self.seleciona_pai()

                print("Pai 1: %", pai1, " - Pai 2: %", pai2)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            nova_populacao = nova_populacao[:-5]
            nova_populacao = nova_populacao + self.populacao[0:5]
            self.populacao = list(nova_populacao)

            self.ordena_populacao()
            self.gerar_probabilidade()
            self.visualiza_geracao()

            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
            self.lista_solucoes.append(melhor.nota_avaliacao)

        self.visualiza_melhor_geracao()
        return self.melhor_solucao
