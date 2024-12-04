from cidade import Cidade
from ag import AlgoritmoGenetico
import matplotlib.pyplot as plt

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
centro_distribuicao = 0

taxa_mutacao = 0.05
numero_geracoes = 100
tamanho_populacao = 16
debug_mode = True

ag = AlgoritmoGenetico(tamanho_populacao, debug_mode)
ag.resolver(taxa_mutacao, numero_geracoes, cidades, rotas, rotas_entrega, centro_distribuicao)

print("\n\n O melhor resultado: \n")
ag.melhor_solucao.print()

plt.plot(ag.lista_solucoes)
plt.title("Acompanhamento dos valores")
plt.show()