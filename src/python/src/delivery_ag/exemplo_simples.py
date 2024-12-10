from cidade import Cidade
from ag import AlgoritmoGenetico
from view import Estatistica

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
