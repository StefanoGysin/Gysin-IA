# -*- coding: utf-8 -*-

"""
Módulo Gerador de Mapa Mental

Este módulo fornece uma classe para criar e manipular mapas mentais usando a biblioteca NetworkX.
Ele permite adicionar conceitos, estabelecer relações entre eles e gerar uma representação visual
do mapa mental.

Autor: [Seu Nome]
Data: [Data de Criação/Atualização]
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List
from utils.logger import configurar_logger

class GeradorMapaMental:
    """
    Classe responsável por gerar e manipular mapas mentais.

    Esta classe utiliza um grafo para representar conceitos e suas relações,
    permitindo a criação de mapas mentais visuais.
    """

    def __init__(self):
        """
        Inicializa o gerador de mapa mental.

        Configura o logger e cria um novo grafo vazio.
        """
        self.logger = configurar_logger("gerador_mapa_mental")
        self.grafo = nx.Graph()

    def adicionar_conceito(self, conceito: str, relacionados: List[str]):
        """
        Adiciona um novo conceito ao mapa mental e suas relações.

        Args:
            conceito (str): O conceito principal a ser adicionado.
            relacionados (List[str]): Lista de conceitos relacionados.
        """
        self.grafo.add_node(conceito)
        for relacionado in relacionados:
            self.grafo.add_edge(conceito, relacionado)
        self.logger.info(f"Adicionado conceito: {conceito} com {len(relacionados)} relações")

    def adicionar_relacao(self, conceito1: str, conceito2: str, peso: float = 1.0):
        """
        Adiciona ou atualiza uma relação entre dois conceitos.

        Args:
            conceito1 (str): Primeiro conceito da relação.
            conceito2 (str): Segundo conceito da relação.
            peso (float, optional): Peso da relação. Padrão é 1.0.
        """
        self.grafo.add_edge(conceito1, conceito2, weight=peso)
        self.logger.info(f"Adicionada relação entre {conceito1} e {conceito2} com peso {peso}")

    def remover_conceito(self, conceito: str):
        """
        Remove um conceito e todas as suas relações do mapa mental.

        Args:
            conceito (str): O conceito a ser removido.
        """
        self.grafo.remove_node(conceito)
        self.logger.info(f"Removido conceito: {conceito}")

    def atualizar_peso_relacao(self, conceito1: str, conceito2: str, novo_peso: float):
        """
        Atualiza o peso da relação entre dois conceitos.

        Args:
            conceito1 (str): Primeiro conceito da relação.
            conceito2 (str): Segundo conceito da relação.
            novo_peso (float): Novo peso da relação.
        """
        self.grafo[conceito1][conceito2]['weight'] = novo_peso
        self.logger.info(f"Atualizado peso da relação entre {conceito1} e {conceito2} para {novo_peso}")

    def obter_conceitos_relacionados(self, conceito: str) -> List[str]:
        """
        Obtém a lista de conceitos diretamente relacionados a um conceito específico.

        Args:
            conceito (str): O conceito para o qual se deseja obter os relacionados.

        Returns:
            List[str]: Lista de conceitos relacionados.
        """
        return list(self.grafo.neighbors(conceito))

    def gerar_mapa(self, arquivo_saida: str = "mapa_mental.png"):
        """
        Gera uma representação visual do mapa mental e salva como imagem.

        Args:
            arquivo_saida (str, optional): Nome do arquivo de saída. Padrão é "mapa_mental.png".
        """
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
        plt.close()
        self.logger.info(f"Mapa mental gerado e salvo em: {arquivo_saida}")

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