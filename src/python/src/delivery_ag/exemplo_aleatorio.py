from random import random

from cidade import Cidade
from ag import AlgoritmoGenetico
from view import Estatistica


def gerar_cidades(numero_cidades: int = 10):
    cidades_array = []

    for i in range(numero_cidades):
        cidades_array.append(Cidade(nome='{}'.format(i)))

    return cidades_array


def gerar_rotas(cidades_rota: list[Cidade]):
    rotas_array = []

    for _ in cidades_rota:
        rota = []

        for j in cidades_rota:
            if random() < 0.4:
                rota.append(-1)
            else:
                rota.append(round(random() * 200) + 1)

        rotas_array.append(rota)
    return rotas_array


def gerar_rotas_entrega(numero_rotas: int,
                        rotas_busca: list[list[int]],
                        index: int = 0,
                        rotas_array: list[int] = None):
    if rotas_array is None:
        rotas_array = []

    if numero_rotas == index:
        return rotas_array

    rota_valida = False
    index_busca = round(random() * (len(rotas_busca) - 1))

    while not rota_valida:
        index_busca = round(random() * (len(rotas_busca) - 1))
        if len(rotas_array) == 0 and rotas_busca[0][index_busca] != -1:
            rota_valida = True

        if len(
                rotas_array) > 0 and rotas_busca[rotas_array[index - 1]][index_busca] != -1:
            rota_valida = True

    rotas_array.append(index_busca)

    return gerar_rotas_entrega(
        numero_rotas,
        rotas_busca,
        index + 1,
        rotas_array)


cidades = gerar_cidades(10)
rotas = gerar_rotas(cidades)
centro_distribuicao = 0

numero_cidades_entrega = round(random() * (len(cidades) / 3)) + 1
rotas_entrega = gerar_rotas_entrega(numero_cidades_entrega, rotas)

taxa_mutacao = 0.05
numero_geracoes = 500
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

print(
    f" ***** (Informações do percurso) *****\n"
    f" Cidade de distribuição: {cidades[centro_distribuicao].nome}\n"
    f" Rota de entrega: {str(rotas_entrega)}\n"
    f" ***** ================ *****\n"
)
print("\n\n O melhor resultado: \n")
ag.melhor_solucao.print()

Estatistica.mostrar_estatistica(
    algoritmo_genetico=ag,
    cidades=cidades,
    rotas=rotas,
    gerar_gif=False,
)
