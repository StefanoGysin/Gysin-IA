import unittest
from core.language_model.modelo_linguagem import ModeloLinguagem
from interface.interface_usuario import InterfaceUsuario
import tkinter as tk

class TestIntegracao(unittest.TestCase):
    def setUp(self):
        self.modelo = ModeloLinguagem()
        self.root = tk.Tk()
        self.interface = InterfaceUsuario(self.root)

    def test_processamento_texto_interface(self):
        texto = "O dia está ótimo para programar em Python!"
        self.interface.entrada.insert(0, texto)
        self.interface.processar_entrada()
        
        output = self.interface.chat_area.get("1.0", tk.END)
        self.assertIn("entidades", output)
        self.assertIn("substantivos", output)
        self.assertIn("verbos", output)
        self.assertIn("sentimento", output)

    def test_modo_aprendizado(self):
        self.interface.modo_aprendizado()
        self.interface.entrada.insert(0, "Estou muito feliz hoje!")
        self.interface.botao_enviar.invoke()
        
        # Simula a entrada do usuário no diálogo de feedback
        self.root.after(100, lambda: self.root.children['!simpledialog'].children['!entry'].insert(0, "positivo"))
        self.root.after(200, lambda: self.root.children['!simpledialog'].ok())
        
        self.root.update()
        
        output = self.interface.chat_area.get("1.0", tk.END)
        self.assertIn("Obrigado pelo feedback", output)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()