# -*- coding: utf-8 -*-

"""
Módulo de testes de integração para a interface do usuário e o modelo de linguagem.

Este módulo contém testes que verificam a interação entre a interface gráfica do usuário
e o processamento de linguagem natural realizado pelo modelo de linguagem.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 2024-10-15 04:28:38 (Zurich)
"""

import pytest
import tkinter as tk
from unittest.mock import patch

from core.language_model.modelo_linguagem import ModeloLinguagem
from interface.interface_usuario import InterfaceUsuario


@pytest.mark.usefixtures("tk_root")
class TestIntegracao:
    """
    Classe de testes de integração para a interface do usuário e o modelo de linguagem.
    """

    @pytest.fixture(autouse=True)
    def setup(self, tk_root):
        """
        Configuração inicial para cada teste.
        
        Args:
            tk_root: Fixture do pytest que fornece uma instância de tk.Tk().
        """
        self.interface = InterfaceUsuario(tk_root)

    def test_processamento_texto_interface(self, tk_root):
        """
        Testa o processamento de texto através da interface do usuário.
        
        Verifica se a saída contém informações sobre entidades, substantivos,
        verbos e sentimento após o processamento do texto de entrada.
        
        Args:
            tk_root: Fixture do pytest para atualização da interface gráfica.
        """
        texto = "O dia está ótimo para programar em Python!"
        self.interface.entrada.insert(0, texto)
        self.interface.processar_entrada()
        tk_root.update()
        
        output = self.interface.chat_area.get("1.0", tk.END)
        assert "entidades" in output
        assert "substantivos" in output
        assert "verbos" in output
        assert "sentimento" in output

    @patch('tkinter.simpledialog.askstring')
    def test_modo_aprendizado(self, mock_askstring, tk_root):
        """
        Testa o modo de aprendizado da interface.
        
        Simula a entrada do usuário e verifica se o feedback é processado corretamente.
        
        Args:
            mock_askstring: Mock para simular a entrada do usuário em uma caixa de diálogo.
            tk_root: Fixture do pytest para atualização da interface gráfica.
        """
        mock_askstring.return_value = "positivo"
        
        self.interface.modo_aprendizado()
        self.interface.entrada.insert(0, "Estou muito feliz hoje!")
        self.interface.botao_enviar.invoke()
        tk_root.update()
        
        output = self.interface.chat_area.get("1.0", tk.END)
        assert "Obrigado pelo feedback" in output