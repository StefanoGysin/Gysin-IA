# core/language_model/modelo_linguagem.py

# Importações necessárias
import spacy
from typing import List, Dict, Any
from utils.logger import configurar_logger
from utils.exceptions import ModeloLinguagemError
from core.memoria import GerenciadorMemoria
from core.mental_map_generator import GeradorMapaMental

class ModeloLinguagem:
    def __init__(self):
        """Inicializa o modelo de linguagem, logger, memória e gerador de mapa mental."""
        self.nlp = spacy.load("pt_core_news_sm")
        self.logger = configurar_logger("modelo_linguagem")
        self.memoria = GerenciadorMemoria()
        self.gerador_mapa = GeradorMapaMental()

    def processar_texto(self, texto: str) -> Dict[str, List[str]]:
        """Processa o texto e extrai informações linguísticas."""
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
        """Analisa o sentimento do texto."""
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
        """Extrai palavras-chave do texto."""
        self.logger.info(f"Extraindo palavras-chave do texto: {texto[:50]}...")
        doc = self.nlp(texto)
        palavras_chave = [token.text for token in doc if not token.is_stop and token.pos_ in ["NOUN", "PROPN", "ADJ"]]
        self.logger.info(f"Palavras-chave extraídas: {palavras_chave}")
        return palavras_chave

    def resumir_texto(self, texto: str, num_sentencas: int = 3) -> str:
        """Resume o texto para um número específico de sentenças."""
        self.logger.info(f"Resumindo texto: {texto[:50]}...")
        doc = self.nlp(texto)
        sentencas = [sent.text for sent in doc.sents]
        resumo = " ".join(sentencas[:num_sentencas])
        self.logger.info(f"Resumo gerado: {resumo}")
        return resumo

    def salvar_informacao(self, chave: str, valor: Any):
        """Salva informações na memória."""
        self.logger.info(f"Salvando informação: {chave}")
        self.memoria.adicionar_informacao(chave, valor)
        self.logger.info(f"Informação salva com sucesso: {chave}")

    def recuperar_informacao(self, chave: str) -> Any:
        """Recupera informações da memória."""
        self.logger.info(f"Recuperando informação: {chave}")
        valor = self.memoria.obter_informacao(chave)
        self.logger.info(f"Informação recuperada: {chave}")
        return valor

    def adicionar_ao_mapa_mental(self, conceito: str, relacionados: List[str]):
        """Adiciona conceitos ao mapa mental."""
        self.logger.info(f"Adicionando conceito ao mapa mental: {conceito}")
        self.gerador_mapa.adicionar_conceito(conceito, relacionados)
        self.logger.info(f"Conceito adicionado com sucesso: {conceito}")

    def gerar_mapa_mental(self, arquivo_saida: str = "mapa_mental.png"):
        """Gera o mapa mental e salva em um arquivo."""
        self.logger.info("Gerando mapa mental")
        self.gerador_mapa.gerar_mapa(arquivo_saida)
        self.logger.info(f"Mapa mental gerado com sucesso: {arquivo_saida}")

    def aprender(self, texto: str, feedback_usuario: str):
        """Aprende com o feedback do usuário."""
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