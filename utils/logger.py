# utils/logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

def configurar_logger(nome_logger: str, nivel: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(nome_logger)
    logger.setLevel(nivel)

    # Se o logger já tem handlers, não adicione novos
    if not logger.handlers:
        # Cria o diretório de logs se não existir
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Configura o manipulador de arquivo
        file_handler = RotatingFileHandler(
            f'logs/{nome_logger}.log',
            maxBytes=1024 * 1024,  # 1 MB
            backupCount=5
        )
        file_handler.setLevel(nivel)

        # Configura o manipulador de console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(nivel)

        # Cria um formatador e adiciona aos manipuladores
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Adiciona os manipuladores ao logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    # Teste básico
    logger = configurar_logger("teste")
    logger.info("Este é um log de informação")
    logger.warning("Este é um log de aviso")
    logger.error("Este é um log de erro")