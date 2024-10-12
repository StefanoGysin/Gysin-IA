# interface/interface_usuario.py

import tkinter as tk
from tkinter import scrolledtext
from core.language_model.modelo_linguagem import ModeloLinguagem

class InterfaceUsuario:
    def __init__(self, master):
        self.master = master
        self.master.title("Gysin-IA: Assistente Virtual")
        self.master.geometry("600x400")

        self.modelo = ModeloLinguagem()

        self.criar_widgets()

    def criar_widgets(self):
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=70, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.entrada = tk.Entry(self.master, width=50)
        self.entrada.grid(row=1, column=0, padx=10, pady=10)

        self.botao_enviar = tk.Button(self.master, text="Enviar", command=self.processar_entrada)
        self.botao_enviar.grid(row=1, column=1, padx=10, pady=10)

    def processar_entrada(self):
        texto_usuario = self.entrada.get()
        self.chat_area.insert(tk.END, f"Você: {texto_usuario}\n")
        
        # Processa o texto usando o modelo de linguagem
        resultado = self.modelo.processar_texto(texto_usuario)
        sentimento = self.modelo.analisar_sentimento(texto_usuario)
        
        # Gera uma resposta simples
        resposta = f"Entendi! Detectei {len(resultado['entidades'])} entidades e {len(resultado['substantivos'])} substantivos. "
        resposta += f"O sentimento parece ser {sentimento}."
        
        self.chat_area.insert(tk.END, f"Gysin-IA: {resposta}\n\n")
        self.entrada.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceUsuario(root)
    root.mainloop()