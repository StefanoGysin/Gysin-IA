# -*- coding: utf-8 -*-
"""
Módulo: chatgpt_integration

Este módulo fornece a classe ChatGPTIntegration, que facilita a integração com a API do OpenAI ChatGPT.
Ele permite a geração de respostas automáticas baseadas em prompts de entrada, utilizando o modelo GPT-3.5-turbo
ou outro modelo especificado.

Autor: Stefano Gysin - StefanoGysin@hotmail.com
Data: 15/10/2024 13:11 (horário de Zurique)

Classes:
    - ChatGPTIntegration

Exceções:
    - ChatGPTIntegrationError

Dependências:
    - openai
    - utils.logger
    - utils.exceptions
"""

import openai
from utils.logger import configurar_logger
from utils.exceptions import ChatGPTIntegrationError

# Define constantes para o modelo e tokens
MODEL_ENGINE = "gpt-3.5-turbo"
DEFAULT_MAX_TOKENS = 150

class ChatGPTIntegration:
    def __init__(self, api_key: str):
        """
        Inicializa a integração com o ChatGPT, configurando a chave da API e o logger.

        :param api_key: Chave da API fornecida pela OpenAI para autenticação
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.logger = configurar_logger("chatgpt_integration")

    def gerar_resposta(self, prompt: str, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
        """
        Gera uma resposta para um dado prompt usando a API do ChatGPT.

        :param prompt: Texto de entrada para o qual se deseja uma resposta
        :param max_tokens: Número máximo de tokens na resposta gerada
        :return: Resposta gerada pelo ChatGPT
        :raises ValueError: Se o prompt for vazio ou max_tokens não for um inteiro positivo
        :raises ChatGPTIntegrationError: Se ocorrer um erro durante a geração da resposta
        """
        if not prompt.strip():
            raise ValueError("O prompt não pode ser vazio")
        
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens deve ser um inteiro positivo")
        
        try:
            self.logger.info(f"Gerando resposta para prompt: {prompt[:50]}...")
            response = self.client.chat.completions.create(
                model=MODEL_ENGINE,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            resposta = response.choices[0].message.content.strip()
            if not resposta:
                raise ChatGPTIntegrationError("A API retornou uma resposta vazia")
            return resposta
        except Exception as e:
            self.logger.error(f"Erro ao gerar resposta: {str(e)}")
            raise ChatGPTIntegrationError(f"Erro ao gerar resposta: {str(e)}")
        finally:
            self.logger.info("Operação de geração de resposta concluída")

    def atualizar_api_key(self, nova_chave: str):
        """
        Atualiza a chave da API usada para autenticação.

        :param nova_chave: A nova chave da API a ser configurada
        """
        self.client = openai.OpenAI(api_key=nova_chave)
        self.logger.info("Chave da API atualizada com sucesso")