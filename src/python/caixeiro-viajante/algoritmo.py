from random import random

from entity import Individuo

class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.lista_solucoes = []
        self.lista_pais = []
        self.melhor_solucao = None

    def inicializa_populacao(self, cidades, rotas, caminho):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(cidades, rotas, caminho))
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
        print(
            " ***** \n",
            "Geração: %s \n" % self.populacao[0].geracao,
            "Melhor solução: %s \n" % self.populacao[0].nota_avaliacao,
            "Melhor Cromossomo: %s \n" % str(self.populacao[0].cromossomo_to_view()),
            "***** \n",
        )

    def gerar_probabilidade(self):
        pesos = [1 / (i_ + 1) for i_ in range(self.tamanho_populacao)]
        soma_pesos = sum(pesos)
        for i_ in range(self.tamanho_populacao):
            self.populacao[i_].probabilidade = (pesos[i_] / soma_pesos) * 100


    def seleciona_pai(self, soma_avaliacao):
        cumulativas = []
        soma = 0
        for i in range(self.tamanho_populacao):
            soma += self.populacao[i].probabilidade
            cumulativas.append(soma)

        numero_aleatorio = round(random() * 100)

        for i, limite in enumerate(cumulativas):
            if numero_aleatorio < limite:
                return i
        return 0

    def resolver(self, taxa_mutacao, numero_geracoes, cidades, rotas, caminho):
        self.inicializa_populacao(cidades, rotas, caminho),
        self.ordena_populacao()
        self.gerar_probabilidade()
        self.visualiza_geracao()
        self.lista_solucoes.append(self.populacao[0].nota_avaliacao)

        for i in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []

            for j in range(self.tamanho_populacao):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)

                self.lista_pais.append(pai1)
                self.lista_pais.append(pai2)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            self.populacao = list(nova_populacao)
            self.ordena_populacao()
            self.gerar_probabilidade()
            self.visualiza_geracao()

            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
            self.lista_solucoes.append(melhor.nota_avaliacao)

        print("\nMelhor solução -> G: %s \nValor: %s \nCromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.cromossomo_to_view()))

        return self.melhor_solucao.cromossomo