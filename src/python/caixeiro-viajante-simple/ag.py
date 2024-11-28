from random import random

from individuo import Individuo

class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, debug_mode = False):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.lista_solucoes = []
        self.lista_pais = []
        self.melhor_solucao = None

        self.debug_mode = debug_mode
        self.debug_populacao = []

    def inicializa_populacao(self, cidades, rotas, caminho):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(cidades, rotas, caminho))
        self.melhor_solucao = self.populacao[0]
        self.debug_populacao.append(self.populacao[0])

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
            self.debug_populacao.append(melhor)
            self.lista_solucoes.append(melhor.nota_avaliacao)

        self.visualiza_melhor_geracao()
        return self.melhor_solucao

class AlgoritmoGeneticoDinamicamente:
    def __init__(self, tamanho_populacao = 100, taxa_mutacao = 0.05, numero_geracoes = 100, debug_mode = False):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.numero_geracoes = numero_geracoes
        self.debug_mode = debug_mode

        self.melhores_resultados = []
        self.melhores_solucoes = []
        self.melhor_solucao = None

        self.debug_populacao = []

    def buscar_melhor_solucao(self, cidades, rotas, rotas_entrega, numero_tentativas = 50):
        self.melhores_resultados = []
        self.melhores_solucoes = []

        for i in range(numero_tentativas):
            ag = AlgoritmoGenetico(self.tamanho_populacao, self.debug_mode)
            ag.resolver(self.taxa_mutacao, self.numero_geracoes, cidades, rotas, rotas_entrega)

            self.melhores_resultados.append(ag.melhor_solucao)
            self.melhores_solucoes.append(ag.melhor_solucao.nota_avaliacao)
            self.debug_populacao = self.debug_populacao + ag.debug_populacao

        self.melhores_resultados = sorted(self.melhores_resultados, key=lambda individuo: individuo.nota_avaliacao, reverse=False)
        self.melhor_solucao = self.melhores_resultados[0]
