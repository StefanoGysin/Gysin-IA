# utils/exceptions.py

class GYSINIAException(Exception):
    """Classe base para exceções personalizadas do GYSIN-IA"""
    pass

class ModeloLinguagemError(GYSINIAException):
    """Exceção levantada para erros relacionados ao modelo de linguagem"""
    pass

class MemoriaError(GYSINIAException):
    """Exceção levantada para erros relacionados ao gerenciamento de memória"""
    pass

class InterfaceUsuarioError(GYSINIAException):
    """Exceção levantada para erros relacionados à interface do usuário"""
    pass

class ChatGPTIntegrationError(GYSINIAException):
    """Exceção levantada para erros relacionados à integração com o ChatGPT"""
    pass