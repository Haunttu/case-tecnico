from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import db, models, auth, user, calls

# Cria as tabelas no banco de dados se não existirem
models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

# Inclui as rotas dos outros arquivos
app.include_router(user.router)
app.include_router(calls.router)


# Rota principal
@app.get("/")
def read_root():
    return {"Status": "API is running"}

# Rota de Login para obter o token
@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db_session: Session = Depends(db.get_db) # get_db vem do módulo db
):
    user = db_session.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.senha_hash):
        raise auth.HTTPException(
            status_code=auth.status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}