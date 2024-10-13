# core/mental_map_generator.py

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List
from utils.logger import configurar_logger

class GeradorMapaMental:
    def __init__(self):
        self.logger = configurar_logger("gerador_mapa_mental")
        self.grafo = nx.Graph()

    def adicionar_conceito(self, conceito: str, relacionados: List[str]):
        self.grafo.add_node(conceito)
        for relacionado in relacionados:
            self.grafo.add_edge(conceito, relacionado)
        self.logger.info(f"Adicionado conceito: {conceito} com {len(relacionados)} relações")

    def adicionar_relacao(self, conceito1: str, conceito2: str, peso: float = 1.0):
        self.grafo.add_edge(conceito1, conceito2, weight=peso)
        self.logger.info(f"Adicionada relação entre {conceito1} e {conceito2} com peso {peso}")

    def remover_conceito(self, conceito: str):
        self.grafo.remove_node(conceito)
        self.logger.info(f"Removido conceito: {conceito}")

    def atualizar_peso_relacao(self, conceito1: str, conceito2: str, novo_peso: float):
        self.grafo[conceito1][conceito2]['weight'] = novo_peso
        self.logger.info(f"Atualizado peso da relação entre {conceito1} e {conceito2} para {novo_peso}")

    def obter_conceitos_relacionados(self, conceito: str) -> List[str]:
        return list(self.grafo.neighbors(conceito))

    def gerar_mapa(self, arquivo_saida: str = "mapa_mental.png"):
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.grafo, k=0.5, iterations=50)
        nx.draw(self.grafo, pos, with_labels=True, node_color='lightblue', 
                node_size=3000, font_size=8, font_weight='bold')
        
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels)
        
        plt.title("Mapa Mental", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
        self.logger.info(f"Mapa mental gerado e salvo em: {arquivo_saida}")

if __name__ == "__main__":
    gerador = GeradorMapaMental()
    gerador.adicionar_conceito("Python", ["Programação", "Linguagem", "Orientação a Objetos"])
    gerador.adicionar_conceito("Programação", ["Algoritmos", "Estruturas de Dados"])
    gerador.adicionar_conceito("Inteligência Artificial", ["Machine Learning", "Redes Neurais", "Processamento de Linguagem Natural"])
    gerador.adicionar_relacao("Python", "Inteligência Artificial", 0.8)
    gerador.atualizar_peso_relacao("Python", "Programação", 1.5)
    gerador.gerar_mapa()
    print(f"Conceitos relacionados a Python: {gerador.obter_conceitos_relacionados('Python')}")