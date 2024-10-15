# -*- coding: utf-8 -*-
"""
Módulo: test_chatgpt_integration

Este módulo contém testes unitários para a classe ChatGPTIntegration, que é responsável por integrar e gerar 
respostas usando a API do ChatGPT. Os testes asseguram que a classe lida corretamente com respostas bem-sucedidas
e erros da API.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 2024-10-15 13:11 (horário de Zurique)

Classes:
    - TestChatGPTIntegration

Exceções:
    - ChatGPTIntegrationError

Dependências:
    - unittest
    - unittest.mock
    - core.chatgpt_integration
    - utils.exceptions
"""

import unittest
from unittest.mock import patch, MagicMock
from core.chatgpt_integration import ChatGPTIntegration
from utils.exceptions import ChatGPTIntegrationError

class TestChatGPTIntegration(unittest.TestCase):
    def setUp(self):
        self.chatgpt = ChatGPTIntegration("fake_api_key")

    @patch('openai.Completion.create')
    def test_gerar_resposta_sucesso(self, mock_create):
        """
        Testa se a função gerar_resposta retorna corretamente uma resposta
        quando a chamada à API do ChatGPT é bem-sucedida.
        """
        mock_response = MagicMock()
        mock_response.choices[0].text = "Esta é uma resposta de teste."
        mock_create.return_value = mock_response

        resposta = self.chatgpt.gerar_resposta("Olá, como você está?")
        self.assertEqual(resposta, "Esta é uma resposta de teste.")

    @patch('openai.Completion.create')
    def test_gerar_resposta_erro(self, mock_create):
        """
        Testa se a função gerar_resposta levanta uma exceção ChatGPTIntegrationError
        quando ocorre um erro na chamada à API do ChatGPT.
        """
        mock_create.side_effect = Exception("Erro de API")

        with self.assertRaises(ChatGPTIntegrationError):
            self.chatgpt.gerar_resposta("Olá, como você está?")

@patch('openai.Completion.create')
def test_gerar_resposta_diferentes_entradas(self, mock_create):
    """Testa gerar_resposta com diferentes tipos de entrada."""
    mock_response = MagicMock()
    mock_response.choices[0].text = "Resposta"
    mock_create.return_value = mock_response

    entradas = ["Texto normal", "123", "!@#$%^&*()"]
    for entrada in entradas:
        with self.subTest(entrada=entrada):
            resposta = self.chatgpt.gerar_resposta(entrada)
            self.assertEqual(resposta, "Resposta")

    # Teste para entrada vazia
    with self.assertRaises(ValueError):
        self.chatgpt.gerar_resposta("")

@patch('openai.Completion.create')
def test_gerar_resposta_vazia(self, mock_create):
    """Testa o comportamento quando a API retorna uma resposta vazia."""
    mock_response = MagicMock()
    mock_response.choices[0].text = ""
    mock_create.return_value = mock_response

    with self.assertRaises(ChatGPTIntegrationError):
        self.chatgpt.gerar_resposta("Teste")

    @patch('openai.Completion.create')
    def test_gerar_resposta_erro_mensagem(self, mock_create):
        """Testa se a mensagem de erro é corretamente incluída na exceção ChatGPTIntegrationError."""
        erro_mensagem = "Erro de API específico"
        mock_create.side_effect = Exception(erro_mensagem)

        with self.assertRaises(ChatGPTIntegrationError) as context:
            self.chatgpt.gerar_resposta("Teste")
        
        self.assertIn(erro_mensagem, str(context.exception))

    @patch('openai.Completion.create')
    def test_gerar_resposta_max_tokens(self, mock_create):
        """Testa se o parâmetro max_tokens é corretamente utilizado."""
        mock_response = MagicMock()
        mock_response.choices[0].text = "Resposta"
        mock_create.return_value = mock_response

        self.chatgpt.gerar_resposta("Teste", max_tokens=50)
        mock_create.assert_called_with(engine=self.chatgpt.model_engine, prompt="Teste", max_tokens=50)

    @patch('openai.Completion.create')
    def test_model_engine_usage(self, mock_create):
        """Testa se o MODEL_ENGINE correto está sendo usado."""
        mock_response = MagicMock()
        mock_response.choices[0].text = "Resposta"
        mock_create.return_value = mock_response

        self.chatgpt.gerar_resposta("Teste")
        mock_create.assert_called_with(engine=self.chatgpt.model_engine, prompt="Teste", max_tokens=150)

if __name__ == '__main__':
    unittest.main()