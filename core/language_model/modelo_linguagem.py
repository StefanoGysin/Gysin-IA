# -*- coding: utf-8 -*-
"""
Módulo: modelo_linguagem

Este módulo implementa a classe ModeloLinguagem, responsável por processar texto, analisar sentimentos,
extrair palavras-chave, resumir textos, e interagir com um gerenciador de memória e um gerador de mapas mentais.
Além disso, integra-se ao ChatGPT para gerar respostas automáticas.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 2024-10-15 13:11 (horário de Zurique)

Classes:
    - ModeloLinguagem

Exceções:
    - ModeloLinguagemError

Dependências:
    - spacy
    - utils.logger
    - utils.exceptions
    - core.memoria
    - core.mental_map_generator
    - core.chatgpt_integration
"""

# Importações necessárias
import spacy
from typing import List, Dict, Any
from utils.logger import configurar_logger
from utils.exceptions import ModeloLinguagemError
from core.memoria import GerenciadorMemoria
from core.mental_map_generator import GeradorMapaMental
from core.chatgpt_integration import ChatGPTIntegration

class ModeloLinguagem:
    def __init__(self, chatgpt_api_key: str):
        """
        Inicializa o modelo de linguagem, logger, memória, gerador de mapa mental e integra o ChatGPT.

        :param chatgpt_api_key: Chave da API do ChatGPT
        """
        self.nlp = spacy.load("pt_core_news_sm")
        self.logger = configurar_logger("modelo_linguagem")
        self.memoria = GerenciadorMemoria()
        self.gerador_mapa = GeradorMapaMental()
        self.chatgpt = ChatGPTIntegration(api_key=chatgpt_api_key)

    def atualizar_chave_api_chatgpt(self, nova_chave: str):
        """
        Atualiza a chave API do ChatGPT.

        :param nova_chave: A nova chave API a ser usada
        """
        self.chatgpt.atualizar_api_key(nova_chave)
        self.logger.info("Chave API do ChatGPT atualizada com sucesso")

    def processar_texto(self, texto: str) -> Dict[str, List[str]]:
        """
        Processa o texto e extrai informações linguísticas.

        :param texto: Texto a ser processado
        :return: Dicionário contendo entidades, tokens, substantivos e verbos extraídos do texto
        :raises ModeloLinguagemError: Se o texto for vazio ou None
        """
        if not texto:
            raise ModeloLinguagemError("O texto não pode ser vazio ou None")
        
        self.logger.info(f"Processando texto: {texto[:50]}...")
        doc = self.nlp(texto)
        
        resultado = {
            "entidades": [ent.text for ent in doc.ents],
            "tokens": [token.text for token in doc],
            "substantivos": [token.text for token in doc if token.pos_ == "NOUN"],
            "verbos": [token.text for token in doc if token.pos_ == "VERB"]
        }
        
        self.logger.info("Texto processado com sucesso")
        return resultado

    def analisar_sentimento(self, texto: str) -> str:
        """
        Analisa o sentimento do texto.

        :param texto: Texto a ser analisado
        :return: Sentimento classificado como 'positivo', 'negativo' ou 'neutro'
        :raises ValueError: Se o texto for vazio
        """
        if not texto:
            raise ValueError("O texto não pode ser vazio")
        
        self.logger.info(f"Analisando sentimento do texto: {texto[:50]}...")
        
        palavras_positivas = ['bom', 'ótimo', 'excelente', 'maravilhoso', 'feliz', 'alegre']
        palavras_negativas = ['ruim', 'péssimo', 'terrível', 'horrível', 'triste', 'infeliz']
        
        contagem_positiva = sum(1 for palavra in palavras_positivas if palavra in texto.lower())
        contagem_negativa = sum(1 for palavra in palavras_negativas if palavra in texto.lower())
        
        if contagem_positiva > contagem_negativa:
            sentimento = "positivo"
        elif contagem_negativa > contagem_positiva:
            sentimento = "negativo"
        else:
            sentimento = "neutro"
        
        self.logger.info(f"Sentimento analisado: {sentimento}")
        return sentimento

    def extrair_palavras_chave(self, texto: str) -> List[str]:
        """
        Extrai palavras-chave do texto.

        :param texto: O texto do qual extrair palavras-chave
        :return: Uma lista de palavras-chave extraídas
        :raises ValueError: Se o texto estiver vazio
        """
        if not texto:
            raise ValueError("O texto não pode ser vazio")
        
        self.logger.info(f"Extraindo palavras-chave do texto: {texto[:50]}...")
        doc = self.nlp(texto)
        palavras_chave = [token.text for token in doc if not token.is_stop and token.pos_ in ["NOUN", "PROPN", "ADJ"]]
        self.logger.info(f"Palavras-chave extraídas: {palavras_chave}")
        return palavras_chave

    def resumir_texto(self, texto: str, num_sentencas: int = 3) -> str:
        """
        Resume o texto para um número específico de sentenças.

        :param texto: Texto a ser resumido
        :param num_sentencas: Número de sentenças desejadas no resumo
        :return: Resumo do texto
        :raises ValueError: Se texto for vazio ou num_sentencas não for um inteiro positivo
        """
        if not texto:
            raise ValueError("O texto não pode ser vazio")
        if not isinstance(num_sentencas, int) or num_sentencas <= 0:
            raise ValueError("num_sentencas deve ser um inteiro positivo")
        
        self.logger.info(f"Resumindo texto: {texto[:50]}...")
        doc = self.nlp(texto)
        sentencas = [sent.text for sent in doc.sents]
        resumo = " ".join(sentencas[:num_sentencas])
        self.logger.info(f"Resumo gerado: {resumo}")
        return resumo

    def salvar_informacao(self, chave: str, valor: Any):
        """
        Salva informações na memória.

        :param chave: Chave para identificar a informação
        :param valor: Valor da informação a ser salva
        :raises ValueError: Se a chave for vazia
        :raises ModeloLinguagemError: Se ocorrer um erro ao salvar a informação
        """
        if not chave:
            raise ValueError("A chave não pode ser vazia")
        try:
            self.logger.info(f"Salvando informação: {chave}")
            self.memoria.adicionar_informacao(chave, valor)
            self.logger.info(f"Informação salva com sucesso: {chave}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar informação: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao salvar informação: {str(e)}")

    def recuperar_informacao(self, chave: str) -> Any:
        """
        Recupera informações da memória.

        :param chave: Chave para identificar a informação
        :return: Valor da informação recuperada
        :raises ValueError: Se a chave for vazia
        :raises ModeloLinguagemError: Se ocorrer um erro ao recuperar a informação
        """
        if not chave:
            raise ValueError("A chave não pode ser vazia")
        try:
            self.logger.info(f"Recuperando informação: {chave}")
            valor = self.memoria.obter_informacao(chave)
            self.logger.info(f"Informação recuperada: {chave}")
            return valor
        except Exception as e:
            self.logger.error(f"Erro ao recuperar informação: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao recuperar informação: {str(e)}")

    def obter_todas_informacoes(self) -> Dict[str, Any]:
        """
        Recupera todas as informações armazenadas na memória.

        :return: Um dicionário com todas as informações armazenadas
        :raises ModeloLinguagemError: Se ocorrer um erro ao recuperar as informações
        """
        try:
            return self.memoria.obter_todas_informacoes()
        except Exception as e:
            self.logger.error(f"Erro ao recuperar todas as informações: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao recuperar todas as informações: {str(e)}")

    def limpar_memoria(self):
        """Limpa todas as informações armazenadas na memória."""
        try:
            self.memoria.limpar_memoria()
            self.logger.info("Memória limpa com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao limpar memória: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao limpar memória: {str(e)}")

    def adicionar_ao_mapa_mental(self, conceito: str, relacionados: List[str]):
        """
        Adiciona um conceito ao mapa mental, junto com conceitos relacionados.

        :param conceito: Conceito principal a ser adicionado
        :param relacionados: Lista de conceitos relacionados
        :raises ValueError: Se o conceito for vazio
        :raises TypeError: Se relacionados não for uma lista de strings
        """
        if not conceito:
            raise ValueError("O conceito não pode ser vazio")
        if not isinstance(relacionados, list):
            raise TypeError("relacionados deve ser uma lista de strings")
        
        self.logger.info(f"Adicionando conceito ao mapa mental: {conceito}")
        self.logger.debug(f"Conceitos relacionados: {relacionados}")
        self.gerador_mapa.adicionar_conceito(conceito, relacionados)
        self.logger.info(f"Conceito adicionado com sucesso: {conceito}")

    def gerar_mapa_mental(self, arquivo_saida: str = "mapa_mental.png"):
        """
        Gera o mapa mental e salva em um arquivo.

        :param arquivo_saida: Nome do arquivo onde o mapa mental será salvo
        :raises ValueError: Se o nome do arquivo de saída for vazio
        """
        if not arquivo_saida:
            raise ValueError("O nome do arquivo de saída não pode ser vazio")
        
        self.logger.info("Gerando mapa mental")
        self.gerador_mapa.gerar_mapa(arquivo_saida)
        self.logger.info(f"Mapa mental gerado com sucesso: {arquivo_saida}")

    def aprender(self, texto: str, feedback_usuario: str):
        """
        Aprende com o feedback do usuário.

        :param texto: Texto de entrada para análise
        :param feedback_usuario: Feedback fornecido pelo usuário
        :raises ValueError: Se texto ou feedback do usuário forem vazios
        """
        if not texto or not feedback_usuario:
            raise ValueError("Texto e feedback do usuário não podem ser vazios")
        
        self.logger.info(f"Aprendendo com feedback do usuário: {feedback_usuario}")
        resultado = self.processar_texto(texto)
        
        contador = self.memoria.obter_informacao("contador_aprendizado") or 0
        contador += 1
        
        self.salvar_informacao(f"aprendizado_{contador}", {
            "texto": texto,
            "feedback": feedback_usuario,
            "analise": resultado
        })
        
        self.salvar_informacao("contador_aprendizado", contador)
        
        # Espaço para implementar lógica adicional de ajuste do modelo
        self.logger.info(f"Aprendizado #{contador} concluído com sucesso")

    def gerar_resposta_chatgpt(self, texto: str) -> str:
        """
        Gera uma resposta usando o ChatGPT.

        :param texto: Texto de entrada para o qual se deseja uma resposta
        :return: Resposta gerada pelo ChatGPT
        :raises ModeloLinguagemError: Se ocorrer um erro ao gerar a resposta
        """
        try:
            self.logger.info(f"Gerando resposta ChatGPT para: {texto[:50]}...")
            resposta = self.chatgpt.gerar_resposta(texto)
            self.logger.info("Resposta ChatGPT gerada com sucesso")
            return resposta
        except Exception as e:
            self.logger.error(f"Erro ao gerar resposta ChatGPT: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao gerar resposta ChatGPT: {str(e)}")