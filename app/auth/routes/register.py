# ===========================
# auth/routes/register.py
# ===========================
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.schemas.password_handler import get_password_hash
import json
import os

router = APIRouter(prefix="/api",
    tags=["Login"])

class RegisterInput(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: RegisterInput):
    """
       Rota para registrar um novo usuário na API.

    Esta rota permite criar uma nova conta de acesso. Após o registro, o usuário poderá realizar login e acessar rotas protegidas com o token JWT.

    ### Corpo da requisição (JSON):
    ```json
    {
    "username": "seu_usuario",
    "email": "seu_email@example.com",
    "password": "sua_senha_segura"
    }
    curl -X POST "http://localhost:8000/register" \
        -H "Content-Type: application/json" \
        -d '{"username": "joao", "email": "joao@email.com", "password": "senha123"}'
    """
    path = "users.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            users = json.load(f)
    else:
        users = {}

    if user.username in users:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    users[user.username] = {
        "username": user.username,
        "full_name": user.username,
        "email": f"{user.username}@example.com",
        "disabled": False,
        "hashed_password": get_password_hash(user.password)
    }

    with open(path, "w") as f:
        json.dump(users, f, indent=4)

    return {"msg": "Usuário criado com sucesso"}
