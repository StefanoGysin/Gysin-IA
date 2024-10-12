# tests/test_modelo_linguagem.py

import unittest
from core.language_model.modelo_linguagem import ModeloLinguagem

class TestModeloLinguagem(unittest.TestCase):
    def setUp(self):
        self.modelo = ModeloLinguagem()

    def test_processar_texto(self):
        texto = "O gato preto pulou sobre o muro alto."
        resultado = self.modelo.processar_texto(texto)
        
        self.assertIn("entidades", resultado)
        self.assertIn("tokens", resultado)
        self.assertIn("substantivos", resultado)
        self.assertIn("verbos", resultado)
        
        self.assertGreater(len(resultado["tokens"]), 0)
        self.assertIn("gato", resultado["substantivos"])
        self.assertIn("pulou", resultado["verbos"])

    def test_analisar_sentimento(self):
        texto_positivo = "O dia está ótimo!"
        texto_negativo = "Que dia ruim."
        texto_neutro = "O céu está azul."

        self.assertEqual(self.modelo.analisar_sentimento(texto_positivo), "positivo")
        self.assertEqual(self.modelo.analisar_sentimento(texto_negativo), "negativo")
        self.assertEqual(self.modelo.analisar_sentimento(texto_neutro), "neutro")

if __name__ == '__main__':
    unittest.main()