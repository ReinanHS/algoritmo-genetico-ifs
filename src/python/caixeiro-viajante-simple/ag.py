from random import random
from individuo import Individuo


class AlgoritmoGenetico:
    """
    Classe para gerenciar e executar um algoritmo genético.

    Esta implementação permite inicializar uma população de indivíduos, ordenar a população
    por critérios de avaliação, aplicar seleção, crossover e mutação, e identificar a melhor solução
    em um número definido de gerações.

    Parâmetros:
    -----------
    - tamanho_populacao (int): Quantidade de indivíduos na população.
    - taxa_mutacao (float): Taxa de mutação aplicada durante a reprodução.
    - debug_mode (bool): Ativa/desativa mensagens de depuração.
    """

    def __init__(self, tamanho_populacao=20, taxa_mutacao=0.5, debug_mode=False):
        """
        Inicializa a classe com os parâmetros fornecidos.

        Args:
        - tamanho_populacao (int): Tamanho da população inicial.
        - taxa_mutacao (float): Probabilidade de mutação dos genes.
        - debug_mode (bool): Ativa mensagens de depuração para acompanhamento do processo.
        """
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.debug_mode = debug_mode

        self.populacao = []
        self.melhores_solucoes_geracao = []
        self.melhor_solucao = None

    def inicializa_populacao(self, cidades, rotas, caminho, centro_distribuicao):
        """
        Inicializa a população com indivíduos gerados aleatoriamente.

        Args:
        - cidades (list): Lista de cidades do problema.
        - rotas (list): Configuração inicial das rotas disponíveis.
        - caminho (list): Caminho base para o cálculo de distâncias.
        - centro_distribuicao (list): Localização do centro de distribuição.
        """
        for _ in range(self.tamanho_populacao):
            self.populacao.append(Individuo(cidades, rotas, caminho, centro_distribuicao))
        self.melhor_solucao = self.populacao[0]

    def ordena_populacao(self):
        """
        Ordena a população com base na nota de avaliação de cada indivíduo.
        """
        self.populacao.sort(key=lambda individuo: individuo.nota_avaliacao, reverse=False)

    def melhor_individuo(self, individuo):
        """
        Atualiza o melhor indivíduo global baseado na avaliação.

        Args:
        - individuo (Individuo): O indivíduo a ser comparado.
        """
        if individuo.nota_avaliacao < self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self):
        """
        Soma as notas de avaliação de todos os indivíduos na população.

        Returns:
        - (float): Soma das avaliações.
        """
        return sum(individuo.nota_avaliacao for individuo in self.populacao)

    def visualiza_geracao(self):
        """
        Exibe informações sobre a geração atual (somente no modo de depuração).
        """
        if not self.debug_mode:
            return

        melhor = self.populacao[0]
        print(
            f" *****\n"
            f" Geração: {melhor.geracao}\n"
            f" Melhor solução: {melhor.nota_avaliacao}\n"
            f" Distância percorrida: {melhor.distancia_percorrida}\n"
            f" Cidades percorridas: {melhor.cidades_percorridas}\n"
            f" Cromossomo: {melhor.cromossomo_to_view()}\n"
            f" *****"
        )

    def visualiza_melhor_geracao(self):
        """
        Exibe informações sobre o melhor indivíduo encontrado até o momento (modo de depuração).
        """
        if not self.debug_mode:
            return

        melhor = self.melhor_solucao
        print(
            f" ***** (Melhor solução) *****\n"
            f" Geração: {melhor.geracao}\n"
            f" Melhor solução: {melhor.nota_avaliacao}\n"
            f" Distância percorrida: {melhor.distancia_percorrida}\n"
            f" Cidades percorridas: {melhor.cidades_percorridas}\n"
            f" Cromossomo: {melhor.cromossomo_to_view()}\n"
            f" ***** ================ *****"
        )

    def gerar_probabilidade(self):
        """
        Calcula as probabilidades de seleção com base no ranking dos indivíduos.
        Exemplo:
            1 = 1 / 1 = 1.00
            2 = 1 / 2 = 0.50
            3 = 1 / 3 = 0.33
            4 = 1 / 4 = 0.25
            5 = 1 / 5 = 0.02
        Após calcular o peso, devemos somar o valor total, no exemplo iremos ter 2,28
        Para calcular a probabilidade é só dividirmos o peso pelo total, exemplo:
            1 = 1.00 / 2,28 = 0,43
            2 = 0.50 / 2,28 = 0,21
            3 = 0.33 / 2,28 = 0,14
            4 = 0.25 / 2,28 = 0,10
            5 = 0,02 / 2,28 = 0,08
        """
        pesos = [1 / (i + 1) for i in range(len(self.populacao))]
        soma_pesos = sum(pesos)

        for i, individuo in enumerate(self.populacao):
            individuo.probabilidade = (pesos[i] / soma_pesos) * 100

    def seleciona_pai(self):
        """
        Seleciona um indivíduo como pai com base nas probabilidades acumuladas.

        Returns:
        - (int): Índice do indivíduo selecionado.
        """
        cumulativas = []
        soma = 0
        for individuo in self.populacao:
            soma += individuo.probabilidade
            cumulativas.append(soma)

        numero_aleatorio = round(random() * 100)
        for i, limite in enumerate(cumulativas):
            if numero_aleatorio < limite:
                return i
        return self.seleciona_pai()

    def resolver(self, numero_geracoes, cidades, rotas, caminho, centro_distribuicao):
        """
        Executa o algoritmo genético para resolver o problema.

        Args:
        - numero_geracoes (int): Quantidade de gerações a serem executadas.
        - cidades: Lista de cidades do problema.
        - rotas: Configuração inicial das rotas disponíveis.
        - caminho: Caminho base para o cálculo de distâncias.
        - centro_distribuicao: Localização do centro de distribuição.

        Returns:
        - (Individuo): O melhor indivíduo encontrado.
        """
        self.inicializa_populacao(cidades, rotas, caminho, centro_distribuicao)
        self.ordena_populacao()
        self.gerar_probabilidade()
        self.visualiza_geracao()
        self.melhores_solucoes_geracao.append(self.populacao[0])

        for _ in range(numero_geracoes):
            nova_populacao = []

            for _ in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai()
                pai2 = self.seleciona_pai()

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                nova_populacao.append(filhos[0].mutacao(self.taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(self.taxa_mutacao))

            # Elitismo: Implementação que o professor pediu na sala de aula
            nova_populacao = nova_populacao[:-5] + self.populacao[:5]
            self.populacao = nova_populacao

            self.ordena_populacao()
            self.gerar_probabilidade()
            self.visualiza_geracao()

            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
            self.melhores_solucoes_geracao.append(melhor)

        self.visualiza_melhor_geracao()
        return self.melhor_solucao
