from fastapi import APIRouter, HTTPException, Depends
from app.models.responses import ScrapingResponse
from app.scrapers.processamento_scraper import ProcessamentoScraper
from app.utils.helpers import valid_is_int
from app.auth.schemas.dependencies import get_current_user
from datetime import datetime

router = APIRouter(
    prefix="/api",
    tags=["Processamento"],
    dependencies=[Depends(get_current_user)],  # <-- exige token em todas as rotas deste router
)

@router.get(
    "/processamento/{ano}/{tipo_processamento}",
    response_model=ScrapingResponse,
    summary="Consultar processamento por ano e tipo",
    responses={
        200: {
            "description": "Dados encontrados com sucesso (live ou cache)."
        },
        400: {
            "description": "Parâmetros inválidos (ano ou tipo_processamento)."
        },
        401: {
            "description": "Não autorizado. Token ausente ou inválido."
        },
        500: {
            "description": "Erro interno ao tentar recuperar os dados."
        },
    }
)
async def route_get_producao_by_year(
    ano: int = datetime.now().year,
    tipo_processamento: str = None,
):
    """
    Rota para obter a quantidade de uvas processadas no Rio Grande do Sul por ano e tipo.

    Esta rota é **protegida** e requer um token JWT válido no header da requisição.

    As categorias disponíveis são:
    - `viniferas`
    - `americanas_hibridas`
    - `uvas_mesa`
    - `sem_classificacao`

    ### Parâmetros:
    - `ano`: Ano da consulta (obrigatório)
    - `tipo_processamento`: Tipo de processamento (obrigatório)

    ### Exemplo de requisição com `curl`:

    ```bash
    curl -X GET "http://localhost:8000/api/exportacao/2022/espumantes" \
        -H "Authorization: Bearer <seu_token>"
    """
    def get_url(year: int, tipo_processamento: str):
        dict_sub_opcao = {
            "viniferas": "subopt_01",
            "americanas_hibridas": "subopt_02",
            "uvas_mesa": "subopt_03",
            "sem_classificacao": "subopt_04"
        }
        sub_opcao = dict_sub_opcao.get(tipo_processamento.lower())
        if not sub_opcao:
            raise HTTPException(status_code=400, detail="Tipo de processamento inválido.")
        if not valid_is_int(year):
            raise HTTPException(status_code=400, detail="Ano inválido.")
        return f"/index.php?opcao=opt_03&subopcao={sub_opcao}&ano={year}"

    url = get_url(ano, tipo_processamento)
    scraper = ProcessamentoScraper()
    try:
        return ScrapingResponse(status="success", data=scraper.get_content(url), source="live")
    except Exception:
        try:
            return ScrapingResponse(status="success", data=scraper.get_cached_content(url), source="cache")
        except Exception as e_cache:
            raise HTTPException(status_code=500, detail=str(e_cache))
