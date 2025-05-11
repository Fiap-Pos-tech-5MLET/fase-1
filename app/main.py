from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.config import get_settings
from app.routes import producao ,processamento, comercializacao

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para extrair informações o site vitibrasil e retornar em JSON",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo rotas
app.include_router(producao.router)
app.include_router(comercializacao.router)
app.include_router(processamento.router)

@app.get("/")
async def root():
    return {"message": "Ok"}
