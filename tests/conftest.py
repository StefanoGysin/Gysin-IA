# -*- coding: utf-8 -*-

"""
Módulo de configuração de testes para integração com a interface Tkinter.

Este módulo fornece uma fixture do pytest que cria uma instância do Tkinter
para ser usada em testes que requerem uma interface gráfica.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 2024-10-15 03:28:38 (Zurich)
"""

import pytest
import tkinter as tk

@pytest.fixture(scope="session")
def tk_root():
    """
    Fixture para criar e gerenciar uma instância Tkinter durante a sessão de testes.

    Esta fixture inicializa o objeto Tkinter, permitindo que testes que
    requerem uma interface gráfica sejam executados. Ao final da sessão de
    testes, ela garante que os recursos são liberados corretamente.

    Yields:
        root: Instância de tk.Tk() para uso nos testes.
    """
    root = tk.Tk()
    yield root
    # Atualiza quaisquer tarefas pendentes antes de destruir o objeto.
    root.update_idletasks()
    # Destroi a janela Tkinter e encerra a aplicação.
    root.destroy()
    root.quit()