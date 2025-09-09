import httpx
from fastapi import APIRouter, Depends, HTTPException

import auth, models
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/calls",
    tags=["External Calls"]
)

EXTERNAL_API_URL = "http://217.196.61.183/calls"

@router.get("/consume")
async def consume_external_api(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Usamos um cliente HTTP assíncrono
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(EXTERNAL_API_URL)
            response.raise_for_status()  # Lança exceção para respostas com erro (4xx ou 5xx)
            
            # Exemplo de como você poderia atualizar o contador de chamadas
            # Aqui, apenas adicionamos uma contagem simples
            if current_user.qnt_chamadas is None:
                current_user.qnt_chamadas = {"total": 1}
            else:
                # O SQLAlchemy não detecta mudanças em sub-elementos de JSON,
                # então precisamos reatribuir o dicionário
                new_qnt = current_user.qnt_chamadas.copy()
                new_qnt["total"] = new_qnt.get("total", 0) + 1
                current_user.qnt_chamadas = new_qnt

            db.add(current_user)
            db.commit()
            
            return response.json()
        
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Erro ao contatar a API externa: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"A API externa retornou um erro: {exc.response.text}")