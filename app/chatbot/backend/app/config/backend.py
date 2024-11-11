import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URL do banco de dados da variável de ambiente, com fallback para SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Define o nível de log com base na variável de ambiente, com padrão "INFO"
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
