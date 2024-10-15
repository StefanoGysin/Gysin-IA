# -*- coding: utf-8 -*-
"""
setup.py

Este módulo é responsável pela configuração do pacote Python 'gysin-ia' usando setuptools. 
Ele especifica os pacotes necessários, as dependências e as configurações extras para o ambiente de desenvolvimento.
Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 15 de outubro de 2024, 02:49 (horário de Zurique)
"""

from setuptools import setup, find_packages

# Configuração do pacote usando setuptools
setup(
    name="gysin-ia",  # Nome do pacote
    version="0.1",  # Versão inicial do pacote
    packages=find_packages(),  # Localiza automaticamente os pacotes Python a serem incluídos

    # Lista de dependências necessárias para a execução do pacote
    install_requires=[
        'spacy',       # Biblioteca para processamento de linguagem natural
        'textblob',    # Biblioteca para processamento de texto e análise de sentimento
        'networkx',    # Biblioteca para criação e manipulação de grafos
        'matplotlib',  # Biblioteca para criação de gráficos e visualizações
    ],

    # Configurações extras, como pacotes adicionais para desenvolvimento
    extras_require={
        'dev': ['pytest'],  # Inclui pytest para testes durante o desenvolvimento
    },
)