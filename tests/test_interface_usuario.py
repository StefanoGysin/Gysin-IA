import unittest
import tkinter as tk
from interface.interface_usuario import InterfaceUsuario

class TestInterfaceUsuario(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = InterfaceUsuario(self.root)

    def test_widgets_creation(self):
        self.assertIsInstance(self.app.chat_area, tk.scrolledtext.ScrolledText)
        self.assertIsInstance(self.app.entrada, tk.Entry)
        self.assertIsInstance(self.app.botao_enviar, tk.Button)
        self.assertIsInstance(self.app.botao_mapa, tk.Button)
        self.assertIsInstance(self.app.botao_aprender, tk.Button)
        self.assertIsInstance(self.app.botao_limpar, tk.Button)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()