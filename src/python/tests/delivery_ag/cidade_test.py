import unittest

from src.delivery_ag.cidade import Cidade


class TestCidade(unittest.TestCase):
    def test_inicializacao_cidade(self):
        nome_cidade = "São Paulo"
        cidade = Cidade(nome_cidade)
        self.assertEqual(
            cidade.nome,
            nome_cidade,
            "O nome da cidade não foi inicializado corretamente")

    def test_nome_cidade_vazio(self):
        nome_cidade = ""
        cidade = Cidade(nome_cidade)
        self.assertEqual(
            cidade.nome,
            nome_cidade,
            "A cidade deve permitir nomes vazios")


if __name__ == '__main__':
    unittest.main()
