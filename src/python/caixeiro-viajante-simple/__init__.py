from entity import Cidade
from algoritmo import AlgoritmoGenetico
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

caminho = [2,3,5]
taxa_mutacao = 0.05
numero_geracoes = 100

melhores_resultados = []
melhores_solucoes = []

for i in range(10):
    ag = AlgoritmoGenetico(20)
    ag.resolver(taxa_mutacao, numero_geracoes, cidades, rotas, caminho)

    melhores_resultados.append(ag.melhor_solucao)
    melhores_solucoes.append(ag.melhor_solucao.nota_avaliacao)

melhores_resultados = sorted(melhores_resultados,key=lambda individuo: individuo.nota_avaliacao,reverse=False)

print("\n\n O melhor resultado: \n")
melhores_resultados[0].print()

plt.plot(melhores_solucoes)
plt.title("Acompanhamento dos valores")
plt.show()
