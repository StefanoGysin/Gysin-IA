# -*- coding: utf-8 -*-
"""
tests/conftest.py

Este módulo configura fixtures para testes usando o pytest, especificamente para a criação e destruição de uma instância raiz do Tkinter.
Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 15 de outubro de 2024, 02:49 (horário de Zurique)
"""

import pytest
import tkinter as tk

@pytest.fixture(scope="session")
def tk_root():
    """
    Fixture do pytest que fornece uma instância do Tkinter.Tk para ser usada em testes.

    Esta fixture cria uma instância raiz do Tkinter antes dos testes e a mantém atualizada durante a sessão de teste.
    Após todos os testes do módulo serem concluídos, a instância é destruída.
    O escopo da fixture é definido como 'session', garantindo que a mesma instância seja usada para todos os testes na sessão de teste.

    :yield: Uma instância do Tkinter.Tk.
    """
    root = tk.Tk()  # Cria a instância raiz do Tkinter
    yield root  # Fornece a instância para uso nos testes
    root.update()  # Atualiza a instância do Tkinter
    root.destroy()  # Destroi a instância após os testes serem concluídos