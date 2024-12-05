import unittest

from src.delivery_ag.individuo import Individuo
from src.delivery_ag.ag import AlgoritmoGenetico
from src.delivery_ag.cidade import Cidade


class TestAlgoritmoGenetico(unittest.TestCase):
    def setUp(self):
        self.cidades = [
            Cidade("X"),
            Cidade("A"),
            Cidade("B"),
            Cidade("C"),
            Cidade("D"),
            Cidade("E"),
        ]
        self.rotas = [
            [-1, 30, 50, 20, -1, -1],
            [30, -1, 10, -1, -1, -1],
            [50, 40, -1, 15, 30, 20],
            [20, -1, 15, -1, -1, -1],
            [-1, -1, 30, -1, -1, -1],
            [-1, -1, 20, -1, -1, -1],
        ]
        self.caminho = [2, 3, 5]
        self.centro_distribuicao = 0

        self.ag = AlgoritmoGenetico(
            tamanho_populacao=10,
            taxa_mutacao=0.2,
            debug_mode=False)

    def test_inicializa_populacao(self):
        self.ag.inicializa_populacao(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        self.assertEqual(len(self.ag.populacao), 10)
        self.assertTrue(all(isinstance(ind, Individuo)
                        for ind in self.ag.populacao))

    def test_ordena_populacao(self):
        self.ag.inicializa_populacao(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )

        for i, ind in enumerate(self.ag.populacao):
            ind.nota_avaliacao = 10 - i
        self.ag.ordena_populacao()
        self.assertTrue(
            all(
                self.ag.populacao[i].nota_avaliacao <= self.ag.populacao[i + 1].nota_avaliacao
                for i in range(len(self.ag.populacao) - 1)
            )
        )

    def test_melhor_individuo_com_valor_baixo(self):
        self.ag.melhor_solucao = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        self.ag.melhor_solucao.nota_avaliacao = 50

        novo_individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        novo_individuo.nota_avaliacao = 30

        self.ag.melhor_individuo(novo_individuo)
        self.assertEqual(self.ag.melhor_solucao.nota_avaliacao, 30)

    def test_melhor_individuo_com_valor_alto(self):
        self.ag.melhor_solucao = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        self.ag.melhor_solucao.nota_avaliacao = 50

        novo_individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        novo_individuo.nota_avaliacao = 60

        self.ag.melhor_individuo(novo_individuo)
        self.assertEqual(self.ag.melhor_solucao.nota_avaliacao, 50)

    def test_soma_avaliacoes(self):
        self.ag.inicializa_populacao(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        for ind in self.ag.populacao:
            ind.nota_avaliacao = 10
        soma = self.ag.soma_avaliacoes()
        self.assertEqual(soma, 100)

    def test_gerar_probabilidade(self):
        self.ag.inicializa_populacao(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        for i, ind in enumerate(self.ag.populacao):
            ind.nota_avaliacao = i + 1
        self.ag.ordena_populacao()
        self.ag.gerar_probabilidade()

        probabilidade_total = sum(
            ind.probabilidade for ind in self.ag.populacao)
        self.assertAlmostEqual(probabilidade_total, 100, delta=0.1)

    def test_seleciona_pai_com_index_valido(self):
        self.ag.inicializa_populacao(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        for ind in self.ag.populacao:
            ind.probabilidade = 10
        indice_pai = self.ag.seleciona_pai()
        self.assertTrue(0 <= indice_pai < len(self.ag.populacao))

    def test_seleciona_pai_com_maior_probabilidade(self):
        self.ag.inicializa_populacao(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )

        probabilidades = [
            50,
            5.55,
            5.55,
            5.55,
            5.55,
            5.55,
            5.55,
            5.55,
            5.55,
            5.55]
        for i, ind in enumerate(self.ag.populacao):
            ind.probabilidade = probabilidades[i % len(probabilidades)]

        selecoes = {i: 0 for i in range(len(self.ag.populacao))}
        numero_iteracoes = 10000

        for _ in range(numero_iteracoes):
            indice_pai = self.ag.seleciona_pai()
            selecoes[indice_pai] += 1

        frequencias = {i: (selecoes[i] /
                           numero_iteracoes) *
                       100 for i in range(len(self.ag.populacao))}

        tolerancia = 2
        for i in range(len(probabilidades)):
            self.assertAlmostEqual(
                frequencias[i],
                probabilidades[i % len(probabilidades)],
                delta=tolerancia,
                msg=f"Frequência observada para o índice {i} ({frequencias[i]:.2f}%) "
                f"não está próxima da probabilidade esperada ({probabilidades[i]}%)"
            )

    def test_resolver_com_um_valor_baixo(self):
        melhor_solucao = self.ag.resolver(
            numero_geracoes=100,
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
        )
        self.assertIsInstance(melhor_solucao, Individuo)
        self.assertEqual(len(self.ag.populacao), 10)

        self.assertLess(melhor_solucao.nota_avaliacao, 400)


if __name__ == '__main__':
    unittest.main()
