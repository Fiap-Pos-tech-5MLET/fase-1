from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.config import get_settings
from app.routes import producao , processamento , comercializacao, exportacao, importacao
from app.auth.routes import login, register  # ← IMPORTANDO AS ROTAS DE AUTENTICAÇÃO

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description= (
    "API para extrair informações do site vitibrasil e retornar em JSON. \n\n"
    "## Autenticação\n\n"
    "Para testar rotas protegidas no Swagger UI:\n"
    "1. Se registrar em /api/register \n"
    "2. Clique em 'Authorize' no topo da página\n"
    "3. Digite suas credenciais (username/password)\n"
    "4. O sistema fará login automaticamente\n"
    "5. Todas as rotas protegidas funcionarão\n"

    # "Para acessar os dados protegidos, você deve: \n"
    # "- Se registrar em /register \n"
    # "- e depois fazer login em /login para obter um token JWT.\n"

      ),
    version="1.0.0",
    tags=["Home"]
)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo rotas de AUTENTICAÇÃO
app.include_router(login.router)
app.include_router(register.router)

# Incluindo rotas da API
app.include_router(producao.router)
app.include_router(comercializacao.router)
app.include_router(processamento.router)
app.include_router(exportacao.router)
app.include_router(importacao.router)

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API Vitibrasil!",
        "info": "Para acessar os dados protegidos, você deve se registrar em /register e depois fazer login em /login para obter um token JWT.",
        "documentação": "/docs"
    }