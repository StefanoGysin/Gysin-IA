# Importações necessárias
import tkinter as tk
from tkinter import scrolledtext, filedialog
from core.language_model.modelo_linguagem import ModeloLinguagem
from utils.logger import configurar_logger
from utils.exceptions import InterfaceUsuarioError

class InterfaceUsuario:
    def __init__(self, master):
        # Configuração inicial da janela
        self.master = master
        self.master.title("Gysin-IA: Assistente Virtual")
        self.master.geometry("800x600")

        # Inicialização do modelo de linguagem e do logger
        self.modelo = ModeloLinguagem()
        self.logger = configurar_logger("interface_usuario")

        # Criação dos elementos da interface
        self.criar_widgets()

    def criar_widgets(self):
        # Método principal para criar todos os widgets da interface
        self.criar_area_chat()
        self.criar_area_entrada()
        self.criar_botoes()

    def criar_area_chat(self):
        # Criação da área de chat com barra de rolagem
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=30)
        self.chat_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    def criar_area_entrada(self):
        # Criação da área de entrada de texto
        self.entrada = tk.Entry(self.master, width=70)
        self.entrada.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.entrada.bind("<Return>", self.processar_entrada)  # Vincula a tecla Enter à função de processamento

    def criar_botoes(self):
        # Criação dos botões da interface
        self.botao_enviar = tk.Button(self.master, text="Enviar", command=self.processar_entrada)
        self.botao_enviar.grid(row=1, column=2, padx=10, pady=10)

        self.botao_mapa = tk.Button(self.master, text="Gerar Mapa Mental", command=self.gerar_mapa_mental)
        self.botao_mapa.grid(row=2, column=0, padx=10, pady=10)

        self.botao_aprender = tk.Button(self.master, text="Modo Aprendizado", command=self.modo_aprendizado)
        self.botao_aprender.grid(row=2, column=1, padx=10, pady=10)

        self.botao_limpar = tk.Button(self.master, text="Limpar Chat", command=self.limpar_chat)
        self.botao_limpar.grid(row=2, column=2, padx=10, pady=10)

    def processar_entrada(self, event=None):
        # Método para processar a entrada do usuário
        try:
            texto_usuario = self.entrada.get()
            if texto_usuario:
                self.chat_area.insert(tk.END, f"Você: {texto_usuario}\n")
                # Aqui você pode adicionar a lógica para processar o texto do usuário
                # Por exemplo:
                # resposta = self.modelo.processar_texto(texto_usuario)
                # self.chat_area.insert(tk.END, f"Gysin-IA: {resposta}\n\n")
                self.entrada.delete(0, tk.END)  # Limpa o campo de entrada
        except Exception as e:
            self.logger.error(f"Erro ao processar entrada: {str(e)}")
            self.chat_area.insert(tk.END, "Gysin-IA: Desculpe, ocorreu um erro ao processar sua entrada.\n\n")

    def gerar_mapa_mental(self):
        # Método para gerar e salvar o mapa mental
        try:
            arquivo_saida = filedialog.asksaveasfilename(defaultextension=".png")
            if arquivo_saida:
                self.modelo.gerar_mapa_mental(arquivo_saida)
                self.chat_area.insert(tk.END, f"Gysin-IA: Mapa mental gerado e salvo em {arquivo_saida}\n\n")
        except Exception as e:
            self.logger.error(f"Erro ao gerar mapa mental: {str(e)}")
            self.chat_area.insert(tk.END, f"Gysin-IA: Desculpe, ocorreu um erro ao gerar o mapa mental.\n\n")

    def modo_aprendizado(self):
        # Método para ativar o modo de aprendizado
        # Implementação futura
        pass

    def limpar_chat(self):
        # Método para limpar a área de chat
        self.chat_area.delete(1.0, tk.END)

# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceUsuario(root)
    root.mainloop()