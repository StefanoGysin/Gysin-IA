# core/language_model/modelo_linguagem.py

import spacy
from typing import List, Dict
from utils.logger import configurar_logger
from utils.exceptions import ModeloLinguagemError
from core.memoria import GerenciadorMemoria

class ModeloLinguagem:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")
        self.logger = configurar_logger("modelo_linguagem")
        self.memoria = GerenciadorMemoria()

    def processar_texto(self, texto: str) -> Dict[str, List[str]]:
        try:
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
        except Exception as e:
            self.logger.error(f"Erro ao processar texto: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao processar texto: {str(e)}")

    def analisar_sentimento(self, texto: str) -> str:
        try:
            self.logger.info(f"Analisando sentimento do texto: {texto[:50]}...")
            # Lógica básica de análise de sentimento
            if "bom" in texto.lower() or "ótimo" in texto.lower():
                sentimento = "positivo"
            elif "ruim" in texto.lower() or "péssimo" in texto.lower():
                sentimento = "negativo"
            else:
                sentimento = "neutro"
            
            self.logger.info(f"Sentimento analisado: {sentimento}")
            return sentimento
        except Exception as e:
            self.logger.error(f"Erro ao analisar sentimento: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao analisar sentimento: {str(e)}")

    def salvar_informacao(self, chave: str, valor: str):
        try:
            self.logger.info(f"Salvando informação: {chave}")
            self.memoria.adicionar_informacao(chave, valor)
            self.logger.info(f"Informação salva com sucesso: {chave}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar informação: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao salvar informação: {str(e)}")

    def recuperar_informacao(self, chave: str) -> str:
        try:
            self.logger.info(f"Recuperando informação: {chave}")
            valor = self.memoria.obter_informacao(chave)
            self.logger.info(f"Informação recuperada: {chave}")
            return valor
        except Exception as e:
            self.logger.error(f"Erro ao recuperar informação: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao recuperar informação: {str(e)}")