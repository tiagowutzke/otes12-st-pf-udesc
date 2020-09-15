import unittest
from datetime import datetime


class Test(unittest.TestCase):

    # Definição das métricas

    @staticmethod
    def medidas_projeto(real_termino, planejada_termino, real_inicio):
        real_termino = datetime.strptime(real_termino, '%Y-%m-%d')
        planejada_termino = datetime.strptime(planejada_termino, '%Y-%m-%d')
        real_inicio = datetime.strptime(real_inicio, '%Y-%m-%d')

        return round((real_termino - planejada_termino) * 100 / (planejada_termino - real_inicio), 2)

    @staticmethod
    def vaf(gsc):
        return round(0.65 + (0.01 * gsc), 2)

    @staticmethod
    def pontos_funcao(ufp, vaf):
        return round(ufp * vaf, 2)

    @staticmethod
    def fator_teste(linhas_teste, linhas_prod):
        return round(linhas_teste / linhas_prod, 2)

    @staticmethod
    def casos_teste(total_teste, linhas_prod):
        return round(total_teste / linhas_prod, 2)

    @staticmethod
    def assertivas(total_assertivas, linhas_prod):
        return round(total_assertivas / linhas_prod, 2)

    @staticmethod
    def assertivas_passando(assertivas_passando, total_assertivas):
        return round(assertivas_passando / total_assertivas, 2)

    @staticmethod
    def assertivas_falhando(assertivas_falhando, total_assertivas):
        return round(assertivas_falhando / total_assertivas, 2)

    @staticmethod
    def aceitacao(casos_atual, casos_anterior):
        return casos_atual - casos_anterior

    @staticmethod
    def aceitacao_passando(aceitacao_passando, aceitacao_total):
        return round(aceitacao_passando / aceitacao_total, 2)

    @staticmethod
    def aceitacao_falhando(aceitacao_falhando, aceitacao_total):
        return round(aceitacao_falhando / aceitacao_total, 2)

    # Execução dos testes unitários

    def test_medidas_projeto(self):
        self.assertEqual(
            self.medidas_projeto(
                real_termino='2020-08-28',
                planejada_termino='2020-08-16',
                real_inicio='2020-06-03'
            ),
            16.22  # esperado
        )

    def test_vaf(self):
        self.assertEqual(
            self.vaf(gsc=47),
            1.12  # esperado
        )

    def test_pontos_funcao(self):
        self.assertEqual(
            self.pontos_funcao(
                ufp=154,
                vaf=1.13
            ),
            174.02  # esperado
        )

    def test_fator_teste(self):
        self.assertEqual(
            self.fator_teste(
                linhas_teste=289,
                linhas_prod=410
            ),
            0.7  # esperado
        )

    def test_casos_teste(self):
        self.assertEqual(
            self.casos_teste(
                total_teste=39,
                linhas_prod=410
            ),
            0.1  # esperado
        )

    def test_assertivas(self):
        self.assertEqual(
            self.assertivas(
                total_assertivas=37,
                linhas_prod=410
            ),
            0.09  # esperado
        )

    def test_assertivas_passando(self):
        self.assertEqual(
            self.assertivas_passando(
                assertivas_passando=25,
                total_assertivas=37
            ),
            0.68  # esperado
        )

    def test_assertivas_falhando(self):
        self.assertEqual(
            self.assertivas_falhando(
                assertivas_falhando=12,
                total_assertivas=37
            ),
            0.32  # esperado
        )

    def test_aceitacao(self):
        self.assertEqual(
            self.aceitacao(
                casos_atual=31,
                casos_anterior=27
            ),
            4  # esperado
        )

    def test_aceitacao_passando(self):
        self.assertEqual(
            self.aceitacao_passando(
                aceitacao_passando=20,
                aceitacao_total=45
            ),
            0.44  # esperado
        )

    def test_aceitacao_falhando(self):
        self.assertEqual(
            self.aceitacao_falhando(
                aceitacao_falhando=25,
                aceitacao_total=45
            ),
            0.56  # esperado
        )


if __name__ == '__main__':
    unittest.main()
