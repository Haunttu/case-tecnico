import os
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from db import get_db
from models import User as UserModel

# --- Configuração de Segurança ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Contexto para Hashing de Senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema do OAuth2 para o Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- Schemas (Modelos Pydantic) para validação ---
class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

class UserCreate(UserBase):
    password: str
    role: str = "User"
    scope: dict = {}
    qnt_chamadas: dict = {}

class UserResponse(UserBase):
    id: int
    role: str
    scope: Optional[dict] = None
    qnt_chamadas: Optional[dict] = None

    class Config:
        orm_mode = True

# --- Funções de Autenticação ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependência para obter o usuário atual ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Dependência para verificar se o usuário é Admin ---
def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: requer privilégios de Administrador."
        )
    return current_user