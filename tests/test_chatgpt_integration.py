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
        """Configura uma instância da integração com ChatGPT para uso nos testes."""
        self.chatgpt = ChatGPTIntegration("fake_api_key")

    @patch('openai.Completion.create')
    def test_gerar_resposta_sucesso(self, mock_create):
        """
        Testa se a função gerar_resposta retorna corretamente uma resposta
        quando a chamada à API do ChatGPT é bem-sucedida.
        """
        # Configura o mock para retornar uma resposta de teste
        mock_response = MagicMock()
        mock_response.choices[0].text = "Esta é uma resposta de teste."
        mock_create.return_value = mock_response

        # Chama a função e verifica se a resposta está correta
        resposta = self.chatgpt.gerar_resposta("Olá, como você está?")
        self.assertEqual(resposta, "Esta é uma resposta de teste.")

    @patch('openai.Completion.create')
    def test_gerar_resposta_erro(self, mock_create):
        """
        Testa se a função gerar_resposta levanta uma exceção ChatGPTIntegrationError
        quando ocorre um erro na chamada à API do ChatGPT.
        """
        # Configura o mock para levantar uma exceção
        mock_create.side_effect = Exception("Erro de API")

        # Verifica se a exceção correta é levantada
        with self.assertRaises(ChatGPTIntegrationError):
            self.chatgpt.gerar_resposta("Olá, como você está?")

if __name__ == '__main__':
    unittest.main()