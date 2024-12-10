from random import random

from cidade import Cidade
from ag import AlgoritmoGenetico
from view import Estatistica

cidades = []
rotas = []

for i in range(10):
    cidades.append(Cidade(nome='Cidade {}'.format(i)))

for i in cidades:
    rota = []

    for j in cidades:
        if random() < 0.3:
            rota.append(-1)
        else:
            rota.append(round(random() * 200) + 1)

    rotas.append(rota)

rotas_entrega = []

for i in range(round(len(cidades) / 2)):
    rotas_entrega.append(
        round(
            random() * (len(cidades) - 1)
        ) + 1
    )

centro_distribuicao = 0

taxa_mutacao = 0.05
numero_geracoes = 400
tamanho_populacao = 20
debug_mode = False

ag = AlgoritmoGenetico(
    tamanho_populacao=tamanho_populacao,
    taxa_mutacao=taxa_mutacao,
    debug_mode=debug_mode,
)

ag.resolver(
    numero_geracoes=numero_geracoes,
    cidades=cidades,
    rotas=rotas,
    caminho=rotas_entrega,
    centro_distribuicao=centro_distribuicao,
)

print("\n\n O melhor resultado: \n")
ag.melhor_solucao.print()

Estatistica.mostrar_estatistica(
    algoritmo_genetico=ag,
    cidades=cidades,
    rotas=rotas,
    gerar_gif=False,
)
