# -*- coding: utf-8 -*-
"""
Módulo: test_interface_usuario

Este módulo contém testes unitários para a classe InterfaceUsuario, que gerencia a interface gráfica do usuário
do assistente virtual Gysin-IA. Os testes verificam a criação correta dos widgets da interface e o processamento
de entrada de texto utilizando funcionalidades do modelo de linguagem.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 2024-10-15 13:11 (horário de Zurique)

Classes:
    - TestInterfaceUsuario

Dependências:
    - unittest
    - tkinter
    - interface.interface_usuario
"""

import unittest
import tkinter as tk
from tkinter import scrolledtext
from interface.interface_usuario import InterfaceUsuario
from unittest.mock import patch, MagicMock

# Constantes para strings repetidas
PYTHON_RESPONSE = "Python é uma ótima linguagem de programação!"
PYTHON_QUERY = "Fale-me sobre Python"

class TestInterfaceUsuario(unittest.TestCase):
    """
    Classe de teste para a InterfaceUsuario.
    
    Esta classe contém métodos de teste para verificar a criação correta dos widgets
    e o funcionamento adequado do processamento de entrada do usuário.
    """

    def setUp(self):
        """
        Configura uma instância da InterfaceUsuario para uso nos testes.
        """
        self.root = tk.Tk()
        self.app = InterfaceUsuario(self.root)

    def test_widgets_creation(self):
        """
        Testa a criação dos widgets da interface para verificar se são instanciados corretamente.
        """
        self.assertIsInstance(self.app.chat_area, scrolledtext.ScrolledText)
        self.assertIsInstance(self.app.entrada, tk.Entry)
        self.assertIsInstance(self.app.botao_enviar, tk.Button)
        self.assertIsInstance(self.app.botao_mapa, tk.Button)
        self.assertIsInstance(self.app.botao_aprender, tk.Button)
        self.assertIsInstance(self.app.botao_limpar, tk.Button)

    @patch('core.language_model.modelo_linguagem.ModeloLinguagem.gerar_resposta_chatgpt')
    @patch('core.language_model.modelo_linguagem.ModeloLinguagem.analisar_sentimento')
    @patch('core.language_model.modelo_linguagem.ModeloLinguagem.processar_texto')
    def test_processar_entrada_com_chatgpt(self, mock_processar, mock_sentimento, mock_chatgpt):
        """
        Testa o processamento de entrada de texto e a integração com o ChatGPT, verificando a resposta
        gerada e a análise de texto.
        """
        # Configura os mocks para retornar valores de teste
        mock_processar.return_value = {
            'entidades': ['Python'],
            'substantivos': ['programação'],
            'verbos': ['é']
        }
        mock_sentimento.return_value = "positivo"
        mock_chatgpt.return_value = PYTHON_RESPONSE

        # Simula a entrada do usuário e processa
        self.app.entrada.insert(0, PYTHON_QUERY)
        self.app.processar_entrada()

        # Obtém e verifica a saída gerada no chat
        output = self.app.chat_area.get("1.0", tk.END)
        self.assertIn(PYTHON_RESPONSE, output)
        self.assertIn("entidades: ['Python']", output)
        self.assertIn("substantivos: ['programação']", output)
        self.assertIn("verbos: ['é']", output)
        self.assertIn("sentimento: positivo", output)

        # Verifica se os métodos mock foram chamados corretamente
        mock_processar.assert_called_once_with(PYTHON_QUERY)
        mock_sentimento.assert_called_once_with(PYTHON_QUERY)
        mock_chatgpt.assert_called_once_with(PYTHON_QUERY)

    def tearDown(self):
        """
        Destroi a janela do Tkinter após cada teste.
        """
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()