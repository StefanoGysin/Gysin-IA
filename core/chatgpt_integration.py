# core/chatgpt_integration.py

import openai
from utils.logger import configurar_logger
from utils.exceptions import ChatGPTIntegrationError

# Define o modelo a ser usado na API do OpenAI
MODEL_ENGINE = "text-davinci-002"
DEFAULT_MAX_TOKENS = 150

class ChatGPTIntegration:
    def __init__(self, api_key: str, openai_client=openai):
        """
        Inicializa a integração com o ChatGPT configurando a chave da API e o logger.

        :param api_key: Chave da API fornecida pela OpenAI para autenticação
        :param openai_client: Cliente OpenAI (padrão é o módulo openai)
        :raises TypeError: Se a chave da API não for uma string
        :raises ValueError: Se a chave da API for vazia
        """
        self._validar_api_key(api_key)
        if not hasattr(openai_client, 'Completion'):
            raise TypeError("openai_client deve ser uma instância válida do cliente OpenAI")
        
        # Configura a chave da API para uso com o OpenAI
        self.openai_client = openai_client
        self.openai_client.api_key = api_key
        self.model_engine = MODEL_ENGINE  # Adicione esta linha
        
        # Configura o logger para esta classe
        self.logger = configurar_logger("chatgpt_integration")

    def _validar_api_key(self, api_key: str):
        """
        Método privado para validar a chave da API.

        :param api_key: Chave da API a ser validada
        :raises TypeError: Se a chave da API não for uma string
        :raises ValueError: Se a chave da API for vazia
        """
        if not isinstance(api_key, str):
            raise TypeError("A chave da API deve ser uma string")
        if not api_key:
            raise ValueError("A chave da API não pode ser vazia")

    def atualizar_api_key(self, nova_chave: str):
        """
        Atualiza a chave da API usada para autenticação.

        :param nova_chave: A nova chave da API a ser configurada
        :raises ValueError: Se a nova chave for vazia
        :raises TypeError: Se a nova chave não for uma string
        """
        self._validar_api_key(nova_chave)
        self.openai_client.api_key = nova_chave
        self.logger.info("Chave da API atualizada com sucesso")

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
            # Loga a tentativa de gerar uma resposta
            self.logger.info(f"Gerando resposta para prompt: {prompt[:50]}...")
            response = self.openai_client.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=max_tokens
            )
            # Extrai a resposta do objeto de resposta da API
            resposta = response.choices[0].text.strip()
            if not resposta:
                raise ChatGPTIntegrationError("A API retornou uma resposta vazia")
            return resposta
        except Exception as e:
            # Loga e levanta um erro se a geração da resposta falhar
            self.logger.error(f"Erro ao gerar resposta: {str(e)}")
            raise ChatGPTIntegrationError(f"Erro ao gerar resposta: {str(e)}")
        finally:
            # Loga a conclusão da operação
            self.logger.info("Operação de geração de resposta concluída")