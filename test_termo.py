import unittest
import termo

class TestTermo(unittest.TestCase):
    def test_trata_palavra(self):
        self.assertEqual(termo.trata_palavra('áéíóúããç'),'aeiouaac')

    def test_palavra_invalida_grande(self):
        self.assertEqual(termo.palavra_invalida('MAISDECINCOCARACTERES'), True)

    def test_palavra_invalida_pequena(self):
        self.assertEqual(termo.palavra_invalida('PEQN'), True)

    def test_palavra_invalida_nao_existe(self):
        self.assertEqual(termo.palavra_invalida('NAOEXISTE'), True)

    def test_acertou(self):
        self.assertEqual(termo.acertou('TESTE', 'TESTE'), True)

    def test_acertou_palavra_com_acento_palpite_sem(self):
        self.assertEqual(termo.acertou('REGUA', 'RÉGUA'), True)

    def test_acertou_palavra_sem_acento_palpite_com(self):
        self.assertEqual(termo.acertou('RÉGUA', 'REGUA'), True)

    def test_acertou_letra_errou_local(self):
        self.assertEqual(termo.acertou_letra_errou_local('E', 'RÉGUA', termo.conta_letras('RÉGUA')), True)

    def test_fim_do_jogo_acertou(self):
        self.assertEqual(termo.fim_do_jogo('REGUA', 'RÉGUA', [1,2,3,4,5,6]), True)
    
    def test_fim_do_jogo_tentativas(self):
        self.assertEqual(termo.fim_do_jogo('TESTE', 'RÉGUA', [1,2,3,4,5,6]), True)

if __name__ == '__main__':
    unittest.main()