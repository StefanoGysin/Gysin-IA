# core/language_model/modelo_linguagem.py

# Importações necessárias
import spacy
from typing import List, Dict
from textblob import TextBlob
from utils.logger import configurar_logger
from utils.exceptions import ModeloLinguagemError
from core.memoria import GerenciadorMemoria
from core.mental_map_generator import GeradorMapaMental

class ModeloLinguagem:
    def __init__(self):
        # Inicialização do modelo de linguagem, logger, memória e gerador de mapa mental
        self.nlp = spacy.load("pt_core_news_sm")
        self.logger = configurar_logger("modelo_linguagem")
        self.memoria = GerenciadorMemoria()
        self.gerador_mapa = GeradorMapaMental()

    def processar_texto(self, texto: str) -> Dict[str, List[str]]:
        # Método para processar o texto e extrair informações linguísticas
        try:
            # Verificação de texto vazio
            if not texto:
                raise ValueError("O texto não pode ser vazio ou None")
            
            self.logger.info(f"Processando texto: {texto[:50]}...")
            doc = self.nlp(texto)
            
            # Extração de entidades, tokens, substantivos e verbos
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
        # Método para analisar o sentimento do texto
        try:
            self.logger.info(f"Analisando sentimento do texto: {texto[:50]}...")
            
            # Listas de palavras positivas e negativas em português
            palavras_positivas = ['bom', 'ótimo', 'excelente', 'maravilhoso', 'feliz', 'alegre']
            palavras_negativas = ['ruim', 'péssimo', 'terrível', 'horrível', 'triste', 'infeliz']
            
            # Contagem de palavras positivas e negativas
            contagem_positiva = sum(1 for palavra in palavras_positivas if palavra in texto.lower())
            contagem_negativa = sum(1 for palavra in palavras_negativas if palavra in texto.lower())
            
            # Determinação do sentimento
            if contagem_positiva > contagem_negativa:
                sentimento = "positivo"
            elif contagem_negativa > contagem_positiva:
                sentimento = "negativo"
            else:
                sentimento = "neutro"
            
            self.logger.info(f"Sentimento analisado: {sentimento}")
            return sentimento
        except Exception as e:
            self.logger.error(f"Erro ao analisar sentimento: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao analisar sentimento: {str(e)}")

    def salvar_informacao(self, chave: str, valor: str):
        # Método para salvar informações na memória
        try:
            self.logger.info(f"Salvando informação: {chave}")
            self.memoria.adicionar_informacao(chave, valor)
            self.logger.info(f"Informação salva com sucesso: {chave}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar informação: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao salvar informação: {str(e)}")

    def recuperar_informacao(self, chave: str) -> str:
        # Método para recuperar informações da memória
        try:
            self.logger.info(f"Recuperando informação: {chave}")
            valor = self.memoria.obter_informacao(chave)
            self.logger.info(f"Informação recuperada: {chave}")
            return valor
        except Exception as e:
            self.logger.error(f"Erro ao recuperar informação: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao recuperar informação: {str(e)}")

    def adicionar_ao_mapa_mental(self, conceito: str, relacionados: List[str]):
        # Método para adicionar conceitos ao mapa mental
        try:
            self.logger.info(f"Adicionando conceito ao mapa mental: {conceito}")
            self.gerador_mapa.adicionar_conceito(conceito, relacionados)
            self.logger.info(f"Conceito adicionado com sucesso: {conceito}")
        except Exception as e:
            self.logger.error(f"Erro ao adicionar conceito ao mapa mental: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao adicionar conceito ao mapa mental: {str(e)}")

    def gerar_mapa_mental(self, arquivo_saida: str = "mapa_mental.png"):
        # Método para gerar o mapa mental
        try:
            self.logger.info("Gerando mapa mental")
            self.gerador_mapa.gerar_mapa(arquivo_saida)
            self.logger.info(f"Mapa mental gerado com sucesso: {arquivo_saida}")
        except Exception as e:
            self.logger.error(f"Erro ao gerar mapa mental: {str(e)}")
            raise ModeloLinguagemError(f"Erro ao gerar mapa mental: {str(e)}")

    def aprender(self, texto: str, feedback_usuario: str):
        # Método para aprender com o feedback do usuário
        try:
            self.logger.info(f"Aprendendo com feedback do usuário: {feedback_usuario}")
            resultado = self.processar_texto(texto)
            
            # Recupera e atualiza o contador de aprendizado
            contador = self.memoria.obter_informacao("contador_aprendizado") or 0
            contador += 1
            
            # Salva o texto, feedback e análise para aprendizado futuro
            self.salvar_informacao(f"aprendizado_{contador}", {
                "texto": texto,
                "feedback": feedback_usuario,
                "analise": resultado
            })
            
            # Atualiza o contador na memória
            self.salvar_informacao("contador_aprendizado", contador)
            
            # Espaço para implementar lógica adicional de ajuste do modelo
            
            self.logger.info(f"Aprendizado #{contador} concluído com sucesso")
        except Exception as e:
            self.logger.error(f"Erro durante o aprendizado: {str(e)}")
            raise ModeloLinguagemError(f"Erro durante o aprendizado: {str(e)}")