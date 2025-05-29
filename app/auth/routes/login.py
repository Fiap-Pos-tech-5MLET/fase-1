# auth/routes/login.py
import os
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta

from app.auth.schemas.password_handler import verify_password
from app.auth.schemas.jwt_handler import create_access_token
from app.auth.schemas.token import Token
from app.auth.schemas.dependencies import get_user

from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter(prefix="/api",
    tags=["Login"])

class LoginInput(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
async def login(credentials: LoginInput):
    """
    Rota para autenticação de usuários via login e geração de token JWT.

    Essa rota verifica as credenciais enviadas e, se estiverem corretas, retorna um token JWT que deverá ser utilizado no cabeçalho (`Authorization`) das requisições às rotas protegidas da API.

    ### Detalhes da requisição:
    - Método: `POST`
    - Endpoint: `/api/login`
    - Tipo de conteúdo: `application/json`
    - Parâmetros:
    - `username`: Nome de usuário registrado.
    - `password`: Senha correspondente ao usuário.

    ### Exemplo de requisição com `curl`:
    ```bash
    curl -X POST "http://localhost:8000/api/login" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"seu_usuario\", \"password\": \"sua_senha\"}"

    """

    return await process_login(credentials.username, credentials.password)

async def process_login(username: str, password: str):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não encontrado"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha incorreta"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
