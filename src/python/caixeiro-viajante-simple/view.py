import matplotlib.pyplot as plt
import networkx as nx
import os
from PIL import Image

class ViewGraph:
    def __init__(self, cidades, rotas, individuo, pos):
        self.cidades = cidades
        self.rotas = rotas
        self.individuo = individuo
        self.caminho_percorrido = []
        self.pos = pos

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

    def desenhar(self, index):
        node_colors = []
        for node in self.graph.nodes:
            if node in self.caminho_percorrido:
                if node == self.caminho_percorrido[0]:
                    node_colors.append("green")
                else:
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

        nx.draw_networkx_edges(self.graph, self.pos, edgelist=normal_edges, alpha=0.7, edge_color='gray')
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=highlighted_edges, width=2.5, edge_color='red')

        if len(self.caminho_percorrido) > 1:
            nx.draw_networkx_edges(
                self.graph, self.pos,
                edgelist=[(self.caminho_percorrido[0], self.caminho_percorrido[1])],
                width=3.5, edge_color='green'
            )

        edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels)

        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            node_color=node_colors,
            node_size=2000,
            font_weight='bold'
        )

        legenda_texto = (
            "Geração: %s\n" % index +
            "Cromossomo: %s\n" % self.individuo.cromossomo_to_view() +
            "Distância percorrida: %s km\n" % self.individuo.distancia_percorrida +
            "Cidades percorridas: %s\n" % self.individuo.cidades_percorridas +
            "Avaliação: %s\n" % self.individuo.nota_avaliacao
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
    def __init__(self, cidades, rotas, melhores_resultados):
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
        frames = []
        for i in range(num_images):
            image_path = f".cache/{i}.png"
            frames.append(Image.open(image_path))

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
        resultados = sorted(resultados, key=lambda individuo: individuo.nota_avaliacao, reverse=True)

        resultados_filtrados = []
        contador_repeticoes = 0
        ultimo_valor = None

        for individuo in resultados:
            if individuo.nota_avaliacao == ultimo_valor:
                contador_repeticoes += 1
            else:
                contador_repeticoes = 1
                ultimo_valor = individuo.nota_avaliacao

            if contador_repeticoes <= 1:
                resultados_filtrados.append(individuo)

        return resultados_filtrados
