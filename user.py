from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, auth
from db import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Rota para criar um usuário novo (apenas Admins)
@router.post("/", response_model=auth.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: auth.UserCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.require_admin) # Garante que só admin pode criar
):
    # Verifica se o email já existe
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        nome=user.nome,
        email=user.email,
        telefone=user.telefone,
        senha_hash=hashed_password,
        role=user.role,
        scope=user.scope,
        qnt_chamadas=user.qnt_chamadas
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Rota para o usuário logado ver seus próprios dados
@router.get("/me", response_model=auth.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# Rota para listar todos os usuários (apenas Admins)
@router.get("/", response_model=List[auth.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.require_admin) # Garante que só admin pode listar todos
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Rota para um usuário editar a própria senha
@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def update_own_password(
    new_password: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    current_user.hashed_password = auth.get_password_hash(new_password)
    db.add(current_user)
    db.commit()
    return {"message": "Senha atualizada com sucesso."}


# Rota para deletar um usuário (apenas Admins)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.require_admin) # Garante que só admin pode deletar
):
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(user_to_delete)
    db.commit()
    return {"ok": True}