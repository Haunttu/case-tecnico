from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.dialects.mysql import JSON as MySQLJSON # Específico para MySQL
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    telefone = Column(String(50))
    senha_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="User")  # "Admin" ou "User"
    scope = Column(MySQLJSON) # Campo JSON
    qnt_chamadas = Column(MySQLJSON) # Campo JSON