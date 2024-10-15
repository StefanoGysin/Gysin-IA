# -*- coding: utf-8 -*-
"""
Módulo: test_modelo_linguagem

Este módulo contém testes unitários para a classe ModeloLinguagem, responsável por processar texto,
analisar sentimentos, interagir com a memória e gerar mapas mentais. Os testes verificam o correto
funcionamento das funcionalidades de processamento de linguagem e integração com o ChatGPT.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 2024-10-15 13:11 (horário de Zurique)

Classes:
    - TestModeloLinguagem

Exceções:
    - ModeloLinguagemError

Dependências:
    - unittest
    - unittest.mock
    - core.language_model.modelo_linguagem
    - utils.exceptions
"""

import os
import unittest
from core.language_model.modelo_linguagem import ModeloLinguagem
from utils.exceptions import ModeloLinguagemError
from unittest.mock import patch, MagicMock

class TestModeloLinguagem(unittest.TestCase):
    def setUp(self):
        """Configura uma instância do ModeloLinguagem para uso nos testes."""
        self.modelo = ModeloLinguagem()

    def test_processar_texto(self):
        """Testa o processamento de texto para verificar se as entidades, tokens, substantivos e verbos são extraídos corretamente."""
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
        """Testa a análise de sentimentos para diferentes tipos de texto."""
        texto_positivo = "O dia está ótimo!"
        texto_negativo = "Que dia ruim."
        texto_neutro = "O céu está azul."

        self.assertEqual(self.modelo.analisar_sentimento(texto_positivo), "positivo")
        self.assertEqual(self.modelo.analisar_sentimento(texto_negativo), "negativo")
        self.assertEqual(self.modelo.analisar_sentimento(texto_neutro), "neutro")

    @patch('core.chatgpt_integration.ChatGPTIntegration.gerar_resposta')
    def test_gerar_resposta_chatgpt(self, mock_gerar_resposta):
        """Testa a geração de resposta do ChatGPT."""
        mock_gerar_resposta.return_value = "Esta é uma resposta de teste do ChatGPT."
        
        resposta = self.modelo.gerar_resposta_chatgpt("Olá, como você está?")
        
        self.assertEqual(resposta, "Esta é uma resposta de teste do ChatGPT.")
        mock_gerar_resposta.assert_called_once_with("Olá, como você está?")

    @patch('core.chatgpt_integration.ChatGPTIntegration.gerar_resposta')
    def test_gerar_resposta_chatgpt_erro(self, mock_gerar_resposta):
        """Testa a geração de resposta do ChatGPT quando ocorre um erro."""
        mock_gerar_resposta.side_effect = Exception("Erro de API")
        
        with self.assertRaises(ModeloLinguagemError):
            self.modelo.gerar_resposta_chatgpt("Olá, como você está?")

    def test_salvar_e_recuperar_informacao(self):
        """Testa o salvamento e a recuperação de informações na memória."""
        chave = "teste_memoria"
        valor = "Isso é um teste"
        
        self.modelo.salvar_informacao(chave, valor)
        resultado = self.modelo.recuperar_informacao(chave)
        
        self.assertEqual(resultado, valor)

    def test_erro_processamento(self):
        """Testa o tratamento de erros no processamento de texto quando o texto é vazio ou None."""
        with self.assertRaises(ModeloLinguagemError):
            self.modelo.processar_texto("")
        
        with self.assertRaises(ModeloLinguagemError):
            self.modelo.processar_texto(None)

    def test_mapa_mental(self):
        """Testa a funcionalidade de geração de mapas mentais e a verificação de conceitos relacionados."""
        conceito = "Python"
        relacionados = ["Programação", "Linguagem", "Orientação a Objetos"]
        self.modelo.adicionar_ao_mapa_mental(conceito, relacionados)
        
        self.modelo.gerar_mapa_mental("test_mapa_mental.png")
        self.assertTrue(os.path.exists("test_mapa_mental.png"))
        
        conceitos_relacionados = self.modelo.gerador_mapa.obter_conceitos_relacionados(conceito)
        self.assertEqual(set(conceitos_relacionados), set(relacionados))

    def tearDown(self):
        """Limpa após cada teste, removendo arquivos de teste gerados."""
        if os.path.exists("test_mapa_mental.png"):
            os.remove("test_mapa_mental.png")

if __name__ == '__main__':
    unittest.main()