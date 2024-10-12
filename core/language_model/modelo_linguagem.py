# core/language_model/modelo_linguagem.py

import spacy
from typing import List, Dict

class ModeloLinguagem:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def processar_texto(self, texto: str) -> Dict[str, List[str]]:
        """
        Processa o texto de entrada e retorna informações linguísticas relevantes.
        
        Args:
            texto (str): O texto a ser processado.
        
        Returns:
            Dict[str, List[str]]: Um dicionário contendo informações linguísticas.
        """
        doc = self.nlp(texto)
        
        return {
            "entidades": [ent.text for ent in doc.ents],
            "tokens": [token.text for token in doc],
            "substantivos": [token.text for token in doc if token.pos_ == "NOUN"],
            "verbos": [token.text for token in doc if token.pos_ == "VERB"]
        }

    def analisar_sentimento(self, texto: str) -> str:
        """
        Analisa o sentimento do texto de entrada.
        
        Args:
            texto (str): O texto a ser analisado.
        
        Returns:
            str: O sentimento do texto (positivo, negativo ou neutro).
        """
        # Implementação simplificada, deve ser aprimorada
        doc = self.nlp(texto)
        
        # Lógica básica de análise de sentimento
        if "bom" in texto.lower() or "ótimo" in texto.lower():
            return "positivo"
        elif "ruim" in texto.lower() or "péssimo" in texto.lower():
            return "negativo"
        else:
            return "neutro"

if __name__ == "__main__":
    modelo = ModeloLinguagem()
    texto_exemplo = "O dia está ótimo para um passeio no parque."
    
    print("Processamento de texto:")
    print(modelo.processar_texto(texto_exemplo))
    
    print("\nAnálise de sentimento:")
    print(modelo.analisar_sentimento(texto_exemplo))