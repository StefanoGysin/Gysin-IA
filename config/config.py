# config/config.py

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Configurações gerais
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Configurações do banco de dados (para uso futuro)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'gysin_ia')
    DB_USER = os.getenv('DB_USER', 'user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

    # Configurações da API (para uso futuro)
    API_KEY = os.getenv('API_KEY', 'sua_chave_api_aqui')

    @staticmethod
    def get_database_url():
        return f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

if __name__ == "__main__":
    print(f"Debug mode: {Config.DEBUG}")
    print(f"Log level: {Config.LOG_LEVEL}")
    print(f"Database URL: {Config.get_database_url()}")