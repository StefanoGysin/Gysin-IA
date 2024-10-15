# -*- coding: utf-8 -*-
"""
core/mental_map_generator.py

Este módulo é responsável por gerar mapas mentais usando a biblioteca NetworkX para representar conceitos e suas relações.
Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 15 de outubro de 2024, 02:49 (horário de Zurique)
"""

# Importações necessárias para manipulação de grafos e visualização
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List
from utils.logger import configurar_logger

class GeradorMapaMental:
    """
    Classe para criar e manipular mapas mentais, permitindo a adição e remoção de conceitos e relações,
    além de gerar uma visualização gráfica do mapa mental.
    """
    
    def __init__(self):
        """Inicializa o gerador de mapa mental com um logger e um grafo vazio."""
        self.logger = configurar_logger("gerador_mapa_mental")
        self.grafo = nx.Graph()

    def adicionar_conceito(self, conceito: str, relacionados: List[str]):
        """
        Adiciona um novo conceito ao grafo e cria arestas para conceitos relacionados.
        
        :param conceito: Nome do conceito a ser adicionado.
        :param relacionados: Lista de conceitos relacionados ao conceito principal.
        """
        self.grafo.add_node(conceito)
        for relacionado in relacionados:
            self.grafo.add_edge(conceito, relacionado)
        self.logger.info(f"Adicionado conceito: {conceito} com {len(relacionados)} relações")

    def adicionar_relacao(self, conceito1: str, conceito2: str, peso: float = 1.0):
        """
        Adiciona uma relação (aresta) entre dois conceitos no grafo com um peso especificado.
        
        :param conceito1: Nome do primeiro conceito.
        :param conceito2: Nome do segundo conceito.
        :param peso: Peso da relação entre os conceitos.
        """
        self.grafo.add_edge(conceito1, conceito2, weight=peso)
        self.logger.info(f"Adicionada relação entre {conceito1} e {conceito2} com peso {peso}")

    def remover_conceito(self, conceito: str):
        """
        Remove um conceito e todas as suas relações do grafo.
        
        :param conceito: Nome do conceito a ser removido.
        """
        self.grafo.remove_node(conceito)
        self.logger.info(f"Removido conceito: {conceito}")

    def atualizar_peso_relacao(self, conceito1: str, conceito2: str, novo_peso: float):
        """
        Atualiza o peso de uma relação existente entre dois conceitos.
        
        :param conceito1: Nome do primeiro conceito.
        :param conceito2: Nome do segundo conceito.
        :param novo_peso: Novo peso para a relação.
        """
        self.grafo[conceito1][conceito2]['weight'] = novo_peso
        self.logger.info(f"Atualizado peso da relação entre {conceito1} e {conceito2} para {novo_peso}")

    def obter_conceitos_relacionados(self, conceito: str) -> List[str]:
        """
        Retorna uma lista de conceitos relacionados a um conceito específico.
        
        :param conceito: Nome do conceito para o qual buscar conceitos relacionados.
        :return: Lista de nomes de conceitos relacionados.
        """
        return list(self.grafo.neighbors(conceito))

    def gerar_mapa(self, arquivo_saida: str = "mapa_mental.png"):
        """
        Gera e salva uma visualização gráfica do mapa mental em um arquivo de imagem.
        
        :param arquivo_saida: Caminho do arquivo onde o mapa será salvo.
        """
        try:
            plt.figure(figsize=(16, 12))
            pos = nx.spring_layout(self.grafo, k=0.5, iterations=50)
            
            # Desenha os nós
            nx.draw_networkx_nodes(self.grafo, pos, node_color='lightblue', node_size=3000, alpha=0.8)
            nx.draw_networkx_labels(self.grafo, pos, font_size=10, font_weight="bold")
            
            # Desenha as arestas
            nx.draw_networkx_edges(self.grafo, pos, edge_color='gray', width=1, alpha=0.5)
            
            # Adiciona pesos nas arestas
            edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
            nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels)
            
            plt.title("Mapa Mental Gysin-IA", fontsize=20)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
            self.logger.info(f"Mapa mental gerado e salvo em: {arquivo_saida}")
        except Exception as e:
            self.logger.error(f"Erro ao gerar mapa mental: {str(e)}")
            raise
        finally:
            plt.close()

if __name__ == "__main__":
    # Exemplo de uso da classe GeradorMapaMental
    gerador = GeradorMapaMental()
    gerador.adicionar_conceito("Python", ["Programação", "Linguagem", "Orientação a Objetos"])
    gerador.adicionar_conceito("Programação", ["Algoritmos", "Estruturas de Dados"])
    gerador.adicionar_conceito("Inteligência Artificial", ["Machine Learning", "Redes Neurais", "Processamento de Linguagem Natural"])
    gerador.adicionar_relacao("Python", "Inteligência Artificial", 0.8)
    gerador.atualizar_peso_relacao("Python", "Programação", 1.5)
    gerador.gerar_mapa()
    print(f"Conceitos relacionados a Python: {gerador.obter_conceitos_relacionados('Python')}")