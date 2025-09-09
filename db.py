import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a "engine" do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Cria uma SessionLocal, que será a sessão de cada requisição
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM (como em models.py)
Base = declarative_base()

# Dependência para obter a sessão do banco em cada rota
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()