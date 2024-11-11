# app/database/database.py
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregar o .env
load_dotenv()

# URL de conexão com o banco de dados
DATABASE_URL = os.environ.get("DATABASE_URL")

# Criar engine e sessão do banco de dados
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=20 - 5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
