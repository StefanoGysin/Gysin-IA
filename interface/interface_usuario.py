# -*- coding: utf-8 -*-
"""
Módulo: interface_usuario

Este módulo implementa a classe InterfaceUsuario, responsável por criar a interface gráfica de usuário (GUI)
para o assistente virtual Gysin-IA. Ele utiliza a biblioteca Tkinter para criar uma janela interativa onde
os usuários podem inserir texto, receber respostas do modelo de linguagem, gerar mapas mentais e interagir
com o sistema de aprendizado.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 15/10/2024 13:11 (horário de Zurique)

Classes:
    - InterfaceUsuario

Exceções:
    - InterfaceUsuarioError
    - ModeloLinguagemError

Dependências:
    - tkinter
    - core.language_model.modelo_linguagem
    - utils.logger
    - utils.exceptions
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, simpledialog, messagebox
from core.language_model.modelo_linguagem import ModeloLinguagem
from utils.logger import configurar_logger
from utils.exceptions import InterfaceUsuarioError, ModeloLinguagemError

# Constantes
TITULO_JANELA = "Gysin-IA: Assistente Virtual"
MENSAGEM_PROCESSANDO = "Gysin-IA: Processando..."
MENSAGEM_ERRO_INESPERADO = "Gysin-IA: Desculpe, ocorreu um erro inesperado."

class InterfaceUsuario:
    def __init__(self, master: tk.Tk) -> None:
        """
        Inicializa a interface do usuário, configurando a janela principal e os componentes.

        :param master: Instância principal da janela do Tkinter
        :raises TypeError: Se master não for uma instância de tk.Tk
        """
        if not isinstance(master, tk.Tk):
            raise TypeError("O parâmetro master deve ser uma instância de tk.Tk")

        self.master = master
        self.master.title(TITULO_JANELA)
        self.master.geometry("800x600")
        self.master.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

        # Centralizar a janela
        self.centralizar_janela()

        # Configurar o logger
        self.logger = configurar_logger("interface_usuario")

        # Inicializar o modelo de linguagem
        try:
            self.modelo = ModeloLinguagem(chatgpt_api_key="sua_chave_api_aqui")
        except Exception as e:
            self.logger.error(f"Erro ao inicializar o ModeloLinguagem: {str(e)}")
            messagebox.showerror("Erro de Inicialização", f"Erro ao inicializar o ModeloLinguagem: {str(e)}")
            raise InterfaceUsuarioError(f"Erro ao inicializar o ModeloLinguagem: {str(e)}")

        # Criar widgets da interface
        self.criar_widgets()
        self.criar_menu() 

    def centralizar_janela(self) -> None:
        """Centraliza a janela na tela."""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def inserir_mensagem(self, mensagem: str) -> None:
        """
        Insere uma mensagem na área de chat e rola para a última mensagem.

        :param mensagem: A mensagem a ser inserida
        """
        self.chat_area.insert(tk.END, mensagem + "\n\n")
        self.chat_area.see(tk.END)

    def tratar_erro(self, mensagem: str, erro: Exception) -> None:
        """Trata erros de forma centralizada, logando e exibindo mensagens."""
        self.logger.error(f"{mensagem}: {str(erro)}")
        self.inserir_mensagem(f"Gysin-IA: {mensagem}: {str(erro)}")

    def validar_entrada(self, texto: str) -> bool:
        """Valida a entrada do usuário."""
        return bool(texto.strip())

    def criar_widgets(self) -> None:
        """Cria todos os widgets da interface."""
        self.criar_area_chat()
        self.criar_area_entrada()
        self.criar_botoes()

    def criar_area_chat(self) -> None:
        """Cria a área de chat com barra de rolagem."""
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=30)
        self.chat_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    def criar_area_entrada(self) -> None:
        """Cria a área de entrada de texto."""
        self.entrada = tk.Entry(self.master, width=70)
        self.entrada.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.entrada.bind("<Return>", self.processar_entrada)

    def criar_botoes(self) -> None:
        """Cria os botões da interface."""
        self.botao_enviar = tk.Button(self.master, text="Enviar", command=self.processar_entrada)
        self.botao_enviar.grid(row=1, column=2, padx=10, pady=10)

        self.botao_mapa = tk.Button(self.master, text="Gerar Mapa Mental", command=self.gerar_mapa_mental)
        self.botao_mapa.grid(row=2, column=0, padx=10, pady=10)

        self.botao_aprender = tk.Button(self.master, text="Modo Aprendizado", command=self.modo_aprendizado)
        self.botao_aprender.grid(row=2, column=1, padx=10, pady=10)

        self.botao_limpar = tk.Button(self.master, text="Limpar Chat", command=self.limpar_chat)
        self.botao_limpar.grid(row=2, column=2, padx=10, pady=10)

        self.botao_atualizar_api = tk.Button(self.master, text="Atualizar Chave API", command=self.atualizar_chave_api)
        self.botao_atualizar_api.grid(row=2, column=3, padx=10, pady=10)

        self.botao_salvar_historico = tk.Button(self.master, text="Salvar Histórico", command=self.salvar_historico)
        self.botao_salvar_historico.grid(row=2, column=4, padx=10, pady=10)

    def criar_menu(self) -> None:
        """Cria o menu da aplicação."""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Salvar Histórico", command=self.salvar_historico)
        arquivo_menu.add_command(label="Limpar Chat", command=self.limpar_chat)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.fechar_aplicacao)

        configuracoes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configurações", menu=configuracoes_menu)
        configuracoes_menu.add_command(label="Atualizar Chave API", command=self.atualizar_chave_api)

    def restaurar_modo_normal(self) -> None:
        """Restaura o modo normal de operação."""
        self.botao_enviar.config(command=self.processar_entrada)
        self.inserir_mensagem("Gysin-IA: Modo normal restaurado.")

    def processar_entrada(self, event: tk.Event = None) -> None:
        """
        Processa a entrada do usuário e gera uma resposta.

        :param event: Evento de teclado (opcional)
        """
        texto_usuario = self.entrada.get().strip()
        if not self.validar_entrada(texto_usuario):
            self.inserir_mensagem("Gysin-IA: Por favor, digite algo antes de enviar.")
            return

        self.inserir_mensagem(f"Você: {texto_usuario}")
        self.inserir_mensagem(MENSAGEM_PROCESSANDO)
        self.master.update_idletasks()

        try:
            resultado = self.modelo.processar_texto(texto_usuario)
            sentimento = self.modelo.analisar_sentimento(texto_usuario)
            resposta_chatgpt = self.modelo.gerar_resposta_chatgpt(texto_usuario)
            
            resposta = f"Gysin-IA: {resposta_chatgpt}\n\n"
            resposta += f"Análise: Detectei {len(resultado['entidades'])} entidades, "
            resposta += f"{len(resultado['substantivos'])} substantivos e {len(resultado['verbos'])} verbos. "
            resposta += f"O sentimento do texto parece ser {sentimento}."
            
            self.chat_area.delete("end-2l", "end-1l")  # Remove a mensagem "Processando..."
            self.inserir_mensagem(resposta)

            if resultado['substantivos']:
                self.modelo.adicionar_ao_mapa_mental(resultado['substantivos'][0], resultado['substantivos'][1:])
            
            self.entrada.delete(0, tk.END)
        except ModeloLinguagemError as e:
            self.chat_area.delete("end-2l", "end-1l")
            self.tratar_erro("Erro no modelo de linguagem", e)
        except ValueError as e:
            self.chat_area.delete("end-2l", "end-1l")
            self.tratar_erro("Erro de valor", e)
        except Exception as e:
            self.chat_area.delete("end-2l", "end-1l")
            self.tratar_erro("Erro inesperado", e)

    def modo_aprendizado(self) -> None:
        """Ativa o modo de aprendizado, solicitando feedback do usuário."""
        def solicitar_feedback():
            texto = self.entrada.get().strip()
            if not texto:
                self.inserir_mensagem("Gysin-IA: Por favor, digite algo antes de enviar feedback.")
                return
            feedback = simpledialog.askstring("Feedback", "Qual é o sentimento correto? (positivo/negativo/neutro)")
            if feedback:
                feedback = feedback.lower()
                if feedback in ["positivo", "negativo", "neutro"]:
                    try:
                        self.modelo.aprender(texto, feedback)
                        self.inserir_mensagem(f"Gysin-IA: Obrigado pelo feedback! Aprendi que '{texto}' tem sentimento {feedback}.")
                    except Exception as e:
                        self.tratar_erro("Erro durante o aprendizado", e)
                        self.inserir_mensagem(f"Gysin-IA: Desculpe, ocorreu um erro durante o aprendizado: {str(e)}")
                else:
                    self.inserir_mensagem("Gysin-IA: Feedback inválido. Por favor, use 'positivo', 'negativo' ou 'neutro'.")
            self.entrada.delete(0, tk.END)

        self.botao_enviar.config(command=solicitar_feedback)
        self.botao_aprender.config(text="Sair do Modo Aprendizado", command=self.restaurar_modo_normal)
        self.inserir_mensagem("Gysin-IA: Modo de aprendizado ativado. Digite uma frase e forneça o sentimento correto.")

    def gerar_mapa_mental(self) -> None:
        """Gera e salva o mapa mental."""
        try:
            arquivo_saida = filedialog.asksaveasfilename(defaultextension=".png")
            if not arquivo_saida:
                return  # O usuário cancelou a operação
            self.modelo.gerar_mapa_mental(arquivo_saida)
            self.inserir_mensagem(f"Gysin-IA: Mapa mental gerado e salvo em {arquivo_saida}")
        except ModeloLinguagemError as e:
            self.tratar_erro("Erro ao gerar mapa mental", e)
        except Exception as e:
            self.tratar_erro("Erro inesperado ao gerar mapa mental", e)

    def atualizar_chave_api(self) -> None:
        """Atualiza a chave API do ChatGPT."""
        nova_chave = simpledialog.askstring("Atualizar Chave API", "Digite a nova chave API:")
        if nova_chave is not None:  # Verifica se o usuário não cancelou o diálogo
            if not nova_chave.strip():
                self.inserir_mensagem("Gysin-IA: A chave API não pode ser vazia.")
                return
            try:
                self.modelo.atualizar_chave_api_chatgpt(nova_chave)
                self.inserir_mensagem("Gysin-IA: Chave API atualizada com sucesso.")
            except Exception as e:
                self.tratar_erro("Erro ao atualizar chave API", e)
        else:
            self.inserir_mensagem("Gysin-IA: Atualização da chave API cancelada.")

    def salvar_historico(self) -> None:
        """Salva o histórico do chat em um arquivo de texto."""
        try:
            arquivo = filedialog.asksaveasfilename(defaultextension=".txt")
            if arquivo:
                with open(arquivo, "w", encoding="utf-8") as f:
                    f.write(self.chat_area.get(1.0, tk.END))
                self.inserir_mensagem(f"Gysin-IA: Histórico salvo em {arquivo}")
        except Exception as e:
            self.tratar_erro("Erro ao salvar histórico", e)

    def limpar_chat(self) -> None:
        """Limpa a área de chat."""
        if messagebox.askyesno("Limpar Chat", "Tem certeza que deseja limpar o chat?"):
            self.chat_area.delete(1.0, tk.END)
            self.inserir_mensagem("Gysin-IA: Chat limpo.")

    def fechar_aplicacao(self) -> None:
        """Fecha a aplicação de forma graciosa."""
        if messagebox.askokcancel("Sair", "Tem certeza que deseja sair?"):
            self.master.destroy()

# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceUsuario(root)
    root.mainloop()