from cidade import Cidade
from ag import AlgoritmoGeneticoDinamicamente
import matplotlib.pyplot as plt
from view import ViewGraph

cidades = [
    Cidade("X"),
    Cidade("A"),
    Cidade("B"),
    Cidade("C"),
    Cidade("D"),
    Cidade("E"),
]

rotas = [
    [-1, 30, 50, 20, -1, -1],
    [30, -1, 10, -1, -1, -1],
    [50, 40, -1, 15, 30, 20],
    [20, -1, 15, -1, -1, -1],
    [-1, -1, 30, -1, -1, -1],
    [-1, -1, 20, -1, -1, -1],
]

rotas_entrega = [2, 3, 5]

taxa_mutacao = 0.05
numero_geracoes = 100
tamanho_populacao = 15
debug_mode = False

ag = AlgoritmoGeneticoDinamicamente(tamanho_populacao, taxa_mutacao, numero_geracoes, debug_mode)
ag.buscar_melhor_solucao(cidades, rotas, rotas_entrega)

print("\n\n O melhor resultado: \n")
ag.melhor_solucao.print()

plt.plot(ag.melhores_solucoes)
plt.title("Acompanhamento dos valores")
plt.show()

view = ViewGraph(cidades, rotas, ag.melhor_solucao)
view.desenhar().show()
