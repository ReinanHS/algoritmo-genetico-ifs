from random import random


class Individuo:
    """
    Representa um indivíduo no algoritmo genético.

    Cada indivíduo é definido por um cromossomo que representa uma rota,
    e seu desempenho é avaliado com base na distância total percorrida,
    número de cidades visitadas, e outras regras do problema.

    Atributos:
    ----------
    - cidades (list): Lista de cidades disponíveis.
    - rotas (list): Matriz representando as distâncias entre as cidades.
    - caminho (list): Lista de cidades obrigatórias a serem visitadas.
    - centro_distribuicao (int): Cidade inicial e final obrigatória no percurso.
    - geracao (int): Número da geração do indivíduo.
    - cromossomo (list): Representação da sequência de cidades percorridas.
    - distancia_percorrida (float): Distância total percorrida.
    - cidades_percorridas (int): Número de cidades diferentes visitadas.
    - nota_avaliacao (float): Avaliação da qualidade da rota.
    """

    def __init__(
            self,
            cidades,
            rotas,
            caminho,
            centro_distribuicao,
            geracao=0,
            cromossomo=None):
        """
        Inicializa o indivíduo com os parâmetros fornecidos.

        Args:
        - cidades (list): Lista de cidades disponíveis.
        - rotas (list): Matriz representando as distâncias entre as cidades.
        - caminho (list): Lista de cidades obrigatórias no percurso.
        - centro_distribuicao (int): Cidade inicial e final obrigatória.
        - geracao (int): Número da geração atual.
        - cromossomo (list): Rota inicial representada como uma sequência de índices.
        """
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
        """
        Gera um cromossomo aleatório representando uma sequência inicial de cidades.
        """
        self.cromossomo = [
            round(random() * (len(self.rotas) - 1))
            for _ in range(len(self.rotas))
        ]

    def avaliacao(self):
        """
        Calcula a nota de avaliação do indivíduo com base no percurso representado pelo cromossomo.

        Penalidades são aplicadas para rotas inválidas ou que não atendam aos requisitos.

        Returns:
        - (float): Nota de avaliação da rota.
        """
        soma_distancia = 0
        cidades_visitadas = []

        for i in range(len(self.cromossomo) - 1):
            origem = self.cromossomo[i]
            destino = self.cromossomo[i + 1]
            distancia = self.rotas[origem][destino]

            soma_distancia += 500 if distancia == -1 else distancia

            if origem in self.caminho and origem not in cidades_visitadas:
                cidades_visitadas.append(origem)

        self.distancia_percorrida = soma_distancia
        self.cidades_percorridas = len(cidades_visitadas)

        # Penalidades por não visitar todas as cidades obrigatórias
        cidades_faltando = len(self.caminho) - len(cidades_visitadas)
        soma_distancia += 100 * cidades_faltando

        # Penalidades por não começar ou terminar no centro de distribuição
        if self.cromossomo[0] != self.centro_distribuicao:
            soma_distancia += 100
        if self.cromossomo[-1] != self.centro_distribuicao:
            soma_distancia += 100

        return soma_distancia

    def crossover(self, outro_individuo):
        """
        Realiza o cruzamento com outro indivíduo para gerar dois filhos.

        Args:
        - outro_individuo (Individuo): Outro indivíduo para cruzamento.

        Returns:
        - (list): Lista com os dois indivíduos filhos gerados.
        """
        corte = round(random() * len(self.cromossomo))
        filho1 = outro_individuo.cromossomo[:corte] + self.cromossomo[corte:]
        filho2 = self.cromossomo[:corte] + outro_individuo.cromossomo[corte:]

        return [
            Individuo(
                self.cidades,
                self.rotas,
                self.caminho,
                self.centro_distribuicao,
                self.geracao + 1,
                filho1),
            Individuo(
                self.cidades,
                self.rotas,
                self.caminho,
                self.centro_distribuicao,
                self.geracao + 1,
                filho2)]

    def mutacao(self, taxa_mutacao):
        """
        Aplica mutação ao cromossomo com base na taxa de mutação fornecida.

        Args:
        - taxa_mutacao (float): Probabilidade de um gene sofrer mutação.

        Returns:
        - (Individuo): O próprio indivíduo com o cromossomo possivelmente alterado.
        """
        for i in range(len(self.cromossomo)):
            if random() <= taxa_mutacao:
                self.cromossomo[i] = round(random() * (len(self.rotas) - 1))

        self.nota_avaliacao = self.avaliacao()
        return self

    def cromossomo_to_view(self):
        """
        Converte o cromossomo para uma representação legível com os nomes das cidades.

        Returns:
        - (list): Lista de nomes das cidades na ordem do cromossomo.
        """
        return [self.cidades[i].nome for i in self.cromossomo]

    def print(self):
        """
        Exibe informações detalhadas do indivíduo, incluindo geração, cromossomo, distância e avaliação.
        """
        print(
            f" ***** \n"
            f" Geração: {self.geracao}\n"
            f" Cromossomo: {self.cromossomo_to_view()}\n"
            f" Distância percorrida: {self.distancia_percorrida}\n"
            f" Cidades percorridas: {self.cidades_percorridas}\n"
            f" Avaliação: {self.nota_avaliacao}\n"
            f" ***** \n"
        )
