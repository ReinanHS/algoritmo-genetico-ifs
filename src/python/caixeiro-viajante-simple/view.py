import matplotlib.pyplot as plt
import networkx as nx

class ViewGraph:
    def __init__(self, cidades, rotas, individuo):
        self.cidades = cidades
        self.rotas = rotas
        self.individuo = individuo
        self.caminho_percorrido = []

        for i in individuo.cromossomo:
            self.caminho_percorrido.append(cidades[i].nome)

        self.graph = nx.Graph()
        self.adicionar_cidade()

    def adicionar_cidade(self):
        for cidade in self.cidades:
            self.graph.add_node(cidade.nome)

        for i in range(len(self.rotas)):
            for j in range(len(self.rotas)):
                if self.rotas[i][j] > 0:
                    self.graph.add_edge(self.cidades[i].nome, self.cidades[j].nome, weight=self.rotas[i][j])

    def desenhar(self):
        pos = nx.spring_layout(self.graph, weight='weight')

        node_colors = []
        for node in self.graph.nodes:
            if node in self.caminho_percorrido:
                node_colors.append("red")
            else:
                node_colors.append("skyblue")

        highlighted_edges = [
            (self.caminho_percorrido[i], self.caminho_percorrido[i + 1])
            for i in range(len(self.caminho_percorrido) - 1)
            if self.graph.has_edge(self.caminho_percorrido[i], self.caminho_percorrido[i + 1])
        ]
        normal_edges = [
            edge for edge in self.graph.edges if edge not in highlighted_edges
        ]

        plt.figure(figsize=(10, 8))

        nx.draw_networkx_edges(self.graph, pos, edgelist=normal_edges, alpha=0.7, edge_color='gray')

        nx.draw_networkx_edges(self.graph, pos, edgelist=highlighted_edges, width=2.5, edge_color='red')

        edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=2000,
            font_weight='bold'
        )

        plt.subplots_adjust(right=0.55)

        legenda_texto = (
            "Cromossomo: %s\n" % self.individuo.cromossomo_to_view() +
            "Distância percorrida: %s km\n" % self.individuo.distancia_percorrida +
            "Cidades percorridas: %s\n" % self.individuo.cidades_percorridas +
            "Avaliação: %s\n" % self.individuo.nota_avaliacao
        )

        plt.text(
            1.0, 0.1, legenda_texto,
            fontsize=14,
            ha='left',
            va='top',
            transform=plt.gca().transAxes,
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.5)
        )

        return plt
