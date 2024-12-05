import unittest
import random

from delivery_ag.cidade import Cidade
from src.delivery_ag.individuo import Individuo


class TestIndividuo(unittest.TestCase):
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

    def test_inicializacao_individuo(self):
        individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao
        )

        self.assertEqual(individuo.cidades, self.cidades)
        self.assertEqual(individuo.rotas, self.rotas)
        self.assertEqual(individuo.caminho, self.caminho)
        self.assertEqual(
            individuo.centro_distribuicao,
            self.centro_distribuicao)
        self.assertEqual(individuo.geracao, 0)
        self.assertEqual(len(individuo.cromossomo), len(self.cidades))

    def test_avaliacao_caminho_perfeito(self):
        individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
            cromossomo=[0, 3, 2, 5, 2, 0]
        )
        nota = individuo.avaliacao()
        self.assertEqual(125, nota)
        self.assertEqual(125, individuo.distancia_percorrida)
        self.assertEqual(3, individuo.cidades_percorridas)
        self.assertEqual(individuo.cromossomo[0], self.centro_distribuicao)
        self.assertEqual(individuo.cromossomo[-1], self.centro_distribuicao)

    def test_avaliacao_caminho_invalido(self):
        individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
            cromossomo=[4, 1, 0, 1, 0, 4]
        )
        nota = individuo.avaliacao()
        self.assertEqual(1590, nota)
        self.assertEqual(1090, individuo.distancia_percorrida)
        self.assertEqual(0, individuo.cidades_percorridas)

    def test_avaliacao_caminho_ruim(self):
        individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
            cromossomo=[0, 1, 2, 4, 2, 0]
        )
        nota = individuo.avaliacao()
        self.assertEqual(350, nota)
        self.assertEqual(150, individuo.distancia_percorrida)
        self.assertEqual(1, individuo.cidades_percorridas)

    def test_crossover(self):
        individuo1 = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
            cromossomo=[1, 4, 4, 2, 3, 2]
        )
        individuo2 = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
            cromossomo=[4, 2, 3, 3, 4, 5]
        )

        random.seed(300)
        filhos = individuo1.crossover(individuo2)
        self.assertEqual(len(filhos), 2)
        self.assertEqual(individuo2.cromossomo[:4], filhos[0].cromossomo[:4])
        self.assertEqual(individuo1.cromossomo[4:], filhos[0].cromossomo[4:])

        self.assertEqual(individuo2.cromossomo[4:], filhos[1].cromossomo[4:])
        self.assertEqual(individuo1.cromossomo[:4], filhos[1].cromossomo[:4])

    def test_mutacao_com_taxa_alta(self):
        individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao
        )
        cromossomo_original = individuo.cromossomo[:]
        nota_original = individuo.nota_avaliacao

        taxa_mutacao = 1.0
        individuo.mutacao(taxa_mutacao)

        self.assertEqual(len(individuo.cromossomo), len(cromossomo_original))
        self.assertNotEqual(individuo.cromossomo, cromossomo_original)
        self.assertNotEqual(individuo.nota_avaliacao, nota_original)

    def test_mutacao_com_taxa_baixa(self):
        individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao
        )
        cromossomo_original = individuo.cromossomo[:]
        nota_original = individuo.nota_avaliacao

        taxa_mutacao = 0.0
        individuo.mutacao(taxa_mutacao)

        self.assertEqual(len(individuo.cromossomo), len(cromossomo_original))
        self.assertEqual(individuo.cromossomo, cromossomo_original)
        self.assertEqual(individuo.nota_avaliacao, nota_original)

    def test_cromossomo_to_view(self):
        individuo = Individuo(
            cidades=self.cidades,
            rotas=self.rotas,
            caminho=self.caminho,
            centro_distribuicao=self.centro_distribuicao,
            cromossomo=[0, 3, 2, 5, 2, 0]
        )
        cromossomo_view = individuo.cromossomo_to_view()
        self.assertEqual(len(cromossomo_view), len(individuo.cromossomo))
        self.assertEqual(['X', 'C', 'B', 'E', 'B', 'X'], cromossomo_view)


if __name__ == '__main__':
    unittest.main()
