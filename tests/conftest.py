# -*- coding: utf-8 -*-

"""
Módulo de configuração de testes para a interface gráfica com Tkinter.

Este módulo define uma fixture para criar e destruir uma instância do Tkinter
para ser usada em testes, garantindo que cada teste tenha seu próprio ambiente de interface gráfica.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 2024-10-15 04:28:38 (Zurich)
"""

import pytest
import tkinter as tk

@pytest.fixture(scope="function")
def tk_root():
    """
    Fixture do pytest para criar uma instância do Tkinter.

    Esta fixture cria uma instância do Tkinter e garante que seja corretamente
    destruída após o término de cada teste.

    Yields:
        root: Instância de tk.Tk() para ser usada nos testes.
    """
    root = tk.Tk()
    yield root
    root.update_idletasks()
    root.destroy()