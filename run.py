import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from interface.interface_usuario import InterfaceUsuario
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceUsuario(root)
    root.mainloop()