# auth/routes/login.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta

from app.auth.schemas.password_handler import verify_password
from app.auth.schemas.jwt_handler import create_access_token
from app.auth.schemas.token import Token
from app.auth.schemas.dependencies import get_user

router = APIRouter(prefix="/api",
    tags=["Login"])

class LoginInput(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
def login(credentials: LoginInput):
    """
    Rota para autenticação de usuários via login e geração de token JWT.

    Essa rota verifica as credenciais enviadas e, se estiverem corretas, retorna um token JWT que deverá ser utilizado no cabeçalho (`Authorization`) das requisições às rotas protegidas da API.

    ### Detalhes da requisição:
    - Método: `POST`
    - Endpoint: `/login`
    - Tipo de conteúdo: `application/x-www-form-urlencoded`
    - Parâmetros:
    - `username`: Nome de usuário registrado.
    - `password`: Senha correspondente ao usuário.

    ### Exemplo de requisição com `curl`:
    ```bash
    curl -X POST "http://localhost:8000/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=seu_usuario&password=sua_senha"

    """
    user = get_user(credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não encontrado"
        )
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha incorreta"
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
