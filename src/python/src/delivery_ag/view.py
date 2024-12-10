import os

import matplotlib.pyplot as plt  
import networkx as nx  
from PIL import Image 


class Estatistica:
    @staticmethod
    def mostrar_estatistica(
            algoritmo_genetico,
            cidades,
            rotas,
            gerar_gif=False):

        pos = ViewGraphEvolution.criar_estrutura_desenho(cidades, rotas)
        view = ViewGraph(
            cidades,
            rotas,
            algoritmo_genetico.melhor_solucao,
            pos)
        view.desenhar(algoritmo_genetico.melhor_solucao.geracao).show()

        plt.plot(
            [individuo.nota_avaliacao for individuo in algoritmo_genetico.historico_populacao])
        plt.title("Histórico de todos os indivíduos")
        plt.show()

        plt.plot(
            [individuo.nota_avaliacao for individuo in algoritmo_genetico.melhores_solucoes_geracao])
        plt.title("Melhores indivíduos por geração")
        plt.show()

        if gerar_gif:
            ViewGraphEvolution(
                cidades, rotas, algoritmo_genetico.melhores_solucoes_geracao)

        pass


class ViewGraph:
    """
    Classe responsável por visualizar o grafo de cidades e rotas de um indivíduo.

    Atributos:
    ----------
    - cidades: Lista de objetos representando as cidades.
    - rotas: Matriz de adjacência representando as distâncias entre as cidades.
    - individuo: Objeto `Individuo` que contém o cromossomo e os dados do percurso.
    - caminho_percorrido: Sequência de nomes das cidades no cromossomo do indivíduo.
    - pos: Posições das cidades no grafo para exibição gráfica.
    - graph: Objeto `networkx.Graph` representando o grafo.
    """

    def __init__(self, cidades, rotas, individuo, pos):
        """
        Inicializa o grafo com as cidades, rotas e o indivíduo a ser visualizado.

        Args:
        - cidades: Lista de objetos representando as cidades.
        - rotas: Matriz de adjacência com as distâncias entre cidades.
        - individuo: Instância de `Individuo` contendo os dados da rota.
        - pos: Posições para exibição gráfica do grafo.
        """
        self.cidades = cidades
        self.rotas = rotas
        self.individuo = individuo
        self.caminho_percorrido = [
            cidades[i].nome for i in individuo.cromossomo]
        self.pos = pos

        self.graph = nx.Graph()
        self.adicionar_cidade()

    def adicionar_cidade(self):
        """
        Adiciona as cidades como nós e as rotas como arestas no grafo.
        """
        for cidade in self.cidades:
            self.graph.add_node(cidade.nome)

        for i in range(len(self.rotas)):
            for j in range(len(self.rotas)):
                if self.rotas[i][j] > 0:
                    self.graph.add_edge(
                        self.cidades[i].nome,
                        self.cidades[j].nome,
                        weight=self.rotas[i][j])

    def desenhar(self, index):
        """
        Desenha o grafo com a rota do indivíduo destacada.

        Args:
        - index (int): Índice da geração atual.

        Returns:
        - (matplotlib.pyplot): Objeto de visualização gráfica.
        """
        node_colors = [
            "green" if node == self.caminho_percorrido[0] else
            "red" if node in self.caminho_percorrido else
            "skyblue"
            for node in self.graph.nodes
        ]

        highlighted_edges = [
            (self.caminho_percorrido[i], self.caminho_percorrido[i + 1])
            for i in range(len(self.caminho_percorrido) - 1)
            if self.graph.has_edge(self.caminho_percorrido[i], self.caminho_percorrido[i + 1])
        ]

        normal_edges = [
            edge for edge in self.graph.edges if edge not in highlighted_edges
        ]

        plt.figure(figsize=(10, 8))

        nx.draw_networkx_edges(
            self.graph,
            self.pos,
            edgelist=normal_edges,
            alpha=0.7,
            edge_color='gray')
        nx.draw_networkx_edges(
            self.graph,
            self.pos,
            edgelist=highlighted_edges,
            width=2.5,
            edge_color='red')

        edge_labels = {(u, v): d['weight']
                       for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(
            self.graph, self.pos, edge_labels=edge_labels)

        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            node_color=node_colors,
            node_size=2000,
            font_weight='bold'
        )

        legenda_texto = (
            f"Geração: {index}\n"
            f"Cromossomo: {self.individuo.cromossomo_to_view()}\n"
            f"Distância percorrida: {self.individuo.distancia_percorrida} km\n"
            f"Cidades percorridas: {self.individuo.cidades_percorridas}\n"
            f"Avaliação: {self.individuo.nota_avaliacao}\n"
        )

        plt.subplots_adjust(right=0.55)
        plt.text(
            1.0, 0.1, legenda_texto,
            fontsize=10,
            ha='left',
            va='top',
            transform=plt.gca().transAxes,
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.5)
        )

        return plt


class ViewGraphEvolution:
    """
    Classe para visualizar a evolução das gerações no algoritmo genético.

    Cria uma sequência de imagens de gráficos para cada geração e os compila em um GIF.

    Atributos:
    ----------
    - cidades: Lista de objetos representando as cidades.
    - rotas: Matriz de adjacência representando as distâncias entre as cidades.
    - melhores_resultados: Lista de indivíduos com as melhores avaliações ao longo das gerações.
    """

    def __init__(self, cidades, rotas, melhores_resultados):
        """
        Inicializa a classe e gera a evolução gráfica.

        Args:
        - cidades: Lista de objetos representando as cidades.
        - rotas: Matriz de adjacência representando as distâncias entre cidades.
        - melhores_resultados: Lista dos melhores indivíduos de cada geração.
        """
        os.makedirs(".cache", exist_ok=True)
        pos = self.criar_estrutura_desenho(cidades, rotas)
        melhores_resultados = self.remover_repeticoes(melhores_resultados)

        for i, individuo in enumerate(melhores_resultados):
            output_path = f".cache/{i}.png"
            view = ViewGraph(cidades, rotas, individuo, pos)
            plt_obj = view.desenhar(i)
            plt_obj.savefig(output_path, format="PNG")
            plt_obj.close()

        self.criar_gif(len(melhores_resultados))

    @staticmethod
    def criar_estrutura_desenho(cidades, rotas):
        """
        Gera posições para o layout gráfico do grafo.

        Args:
        - cidades: Lista de cidades.
        - rotas: Matriz de adjacência com as distâncias.

        Returns:
        - (dict): Posições calculadas para os nós do grafo.
        """
        temp_graph = nx.Graph()
        for cidade in cidades:
            temp_graph.add_node(cidade.nome)
        for i in range(len(rotas)):
            for j in range(len(rotas)):
                if rotas[i][j] > 0:
                    temp_graph.add_edge(cidades[i].nome, cidades[j].nome)
        return nx.spring_layout(temp_graph, weight='weight')

    @staticmethod
    def criar_gif(num_images):
        """
        Compila as imagens das gerações em um GIF.

        Args:
        - num_images (int): Número de imagens geradas.
        """
        frames = [Image.open(f".cache/{i}.png") for i in range(num_images)]

        gif_path = "evolucao.gif"
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=300,
            loop=1
        )
        print(f"GIF salvo em: {gif_path}")

    @staticmethod
    def remover_repeticoes(resultados):
        """
        Remove indivíduos repetidos com a mesma avaliação.

        Args:
        - resultados: Lista de indivíduos.

        Returns:
        - (list): Lista de indivíduos únicos.
        """
        resultados = sorted(
            resultados,
            key=lambda individuo: individuo.nota_avaliacao,
            reverse=True)

        resultados_filtrados = []
        contador_repeticoes = 0
        ultimo_valor = None

        for individuo in resultados:
            if individuo.nota_avaliacao == ultimo_valor:
                contador_repeticoes += 1
            else:
                contador_repeticoes = 1
                ultimo_valor = individuo.nota_avaliacao

            if contador_repeticoes <= 3:
                resultados_filtrados.append(individuo)

        return resultados_filtrados
