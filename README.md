1. Sobre o projeto

Breve descrição do que é o projeto e o que ele faz.
Exemplo:

API desenvolvida com FastAPI, com autenticação JWT, CRUD de usuários e consumo de API externa de chamadas.

2. Pré-requisitos

Liste tudo que a pessoa precisa antes de rodar:

Python 3.10+

MySQL (ou outro banco, se aplicável)

Git

3. Instalação

Passo a passo desde clonar até instalar as dependências:

git clone https://github.com/seu-usuario/case-tecnico-main.git
cd case-tecnico-main/case-tecnico-main
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

4. Configuração

Explique o .env e o banco:

SECRET_KEY="sua_chave"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL="mysql+pymysql://user:senha@localhost:3306/nomedb"


Criar banco no MySQL (CREATE DATABASE nomedb;)

Ajustar usuário e senha do banco

5. Executando o projeto

Como rodar localmente:

uvicorn main:app --reload


Acesse em:

Swagger UI → http://localhost:8000/docs

Redoc → http://localhost:8000/redoc

6. Rotas principais

Liste de forma simples:

Auth: POST /token → login (gera JWT)

Usuários:

POST /users/ (Admin) → criar usuário

GET /users/ (Admin) → listar usuários

GET /users/me → dados do usuário autenticado

PUT /users/{id} → atualizar usuário

DELETE /users/{id} → remover usuário

Chamadas:

GET /calls/consume → consome API externa

7. Testes

Como rodar os testes (se tiver):

pytest
