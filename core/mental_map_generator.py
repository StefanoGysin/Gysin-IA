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

    def gerar_mapa(self, arquivo_saida: str = "mapa_mental.png"):
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.grafo)
        nx.draw(self.grafo, pos, with_labels=True, node_color='lightblue', 
                node_size=3000, font_size=10, font_weight='bold')
        
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels)
        
        plt.title("Mapa Mental", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(arquivo_saida)
        plt.close()
        self.logger.info(f"Mapa mental gerado e salvo em: {arquivo_saida}")

    def obter_conceitos_relacionados(self, conceito: str) -> List[str]:
        return list(self.grafo.neighbors(conceito))

if __name__ == "__main__":
    gerador = GeradorMapaMental()
    gerador.adicionar_conceito("Python", ["Programação", "Linguagem", "Orientação a Objetos"])
    gerador.adicionar_conceito("Programação", ["Algoritmos", "Estruturas de Dados"])
    gerador.adicionar_conceito("Inteligência Artificial", ["Machine Learning", "Redes Neurais", "Processamento de Linguagem Natural"])
    gerador.gerar_mapa()
    print(f"Conceitos relacionados a Python: {gerador.obter_conceitos_relacionados('Python')}")