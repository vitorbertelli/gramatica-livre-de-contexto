import main
import unittest

class TestEliminacaoProducaoInutil(unittest.TestCase):
  def test_um(self):
    gramatica = main.Gramatica.carregar("test_gramaticas/exemplo_eliminacao_producao_inutil.txt")
    resultado = gramatica.eliminar_producoes_inuteis()
    esperado = main.Gramatica.carregar("test_results/resultado_eliminacao_producao_inutil.txt")
    self.assertEqual(resultado, esperado)

  def test_dois(self):
    gramatica = main.Gramatica.carregar("test_gramaticas/exemplo_eliminacao_producao_inutil_2.txt")
    resultado = gramatica.eliminar_producoes_inuteis()
    esperado = main.Gramatica.carregar("test_results/resultado_eliminacao_producao_inutil_2.txt")
    self.assertEqual(resultado, esperado)

  def test_tres(self):
    gramatica = main.Gramatica.carregar("test_gramaticas/exemplo_eliminacao_producao_inutil_2.txt")
    resultado = gramatica.eliminar_producoes_inuteis()
    esperado = main.Gramatica.carregar("test_results/resultado_eliminacao_producao_inutil_2.txt")
    self.assertEqual(resultado, esperado)

class TestEliminacaoProducaoVazia(unittest.TestCase):
  def test_um(self):
    gramatica = main.Gramatica.carregar("test_gramaticas/exemplo_eliminacao_producao_vazia.txt")
    resultado = gramatica.eliminar_producoes_vazias()
    esperado = main.Gramatica.carregar("test_results/resultado_eliminacao_producao_vazia.txt")
    self.assertEqual(resultado, esperado)

  def test_dois(self):
    gramatica = main.Gramatica.carregar("test_gramaticas/exemplo_eliminacao_producao_vazia_2.txt")
    resultado = gramatica.eliminar_producoes_vazias()
    esperado = main.Gramatica.carregar("test_results/resultado_eliminacao_producao_vazia_2.txt")
    self.assertEqual(resultado, esperado)

class TestEliminacaoProducaoUnidade(unittest.TestCase):
  def test_um(self):
    gramatica = main.Gramatica.carregar("test_gramaticas/exemplo_eliminacao_producao_unidade.txt")
    resultado = gramatica.eliminar_producoes_unidades()
    resultado = resultado.eliminar_producoes_inuteis()
    esperado = main.Gramatica.carregar("test_results/resultado_eliminacao_producao_unidade.txt")
    self.assertEqual(resultado, esperado)

if __name__ == '__main__':
  res = unittest.main(verbosity=3, exit=False)