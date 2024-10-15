# tests/test_modelo_linguagem.py

import os
import unittest
from core.language_model.modelo_linguagem import ModeloLinguagem
from utils.exceptions import ModeloLinguagemError


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

    def test_salvar_e_recuperar_informacao(self):
        chave = "teste_memoria"
        valor = "Isso é um teste"
        
        self.modelo.salvar_informacao(chave, valor)
        resultado = self.modelo.recuperar_informacao(chave)
        
        self.assertEqual(resultado, valor)

    def test_erro_processamento(self):
        with self.assertRaises(ModeloLinguagemError):
            self.modelo.processar_texto("")
        
        with self.assertRaises(ModeloLinguagemError):
            self.modelo.processar_texto(None)

    def test_mapa_mental(self):
        conceito = "Python"
        relacionados = ["Programação", "Linguagem", "Orientação a Objetos"]
        self.modelo.adicionar_ao_mapa_mental(conceito, relacionados)
        
        self.modelo.gerar_mapa_mental("test_mapa_mental.png")
        self.assertTrue(os.path.exists("test_mapa_mental.png"))
        
        conceitos_relacionados = self.modelo.gerador_mapa.obter_conceitos_relacionados(conceito)
        self.assertEqual(set(conceitos_relacionados), set(relacionados))

    def tearDown(self):
        # Remover o arquivo de teste após cada teste
        if os.path.exists("test_mapa_mental.png"):
            os.remove("test_mapa_mental.png")

if __name__ == '__main__':
    unittest.main()