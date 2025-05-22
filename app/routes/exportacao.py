from fastapi import APIRouter,  HTTPException, Depends
from app.models.responses import ScrapingResponse
from app.scrapers.exportacao_scraper import ExportacaoScraper
from app.utils.helpers import valid_is_int
from datetime import datetime

from app.auth.schemas.dependencies import get_current_user

router = APIRouter(  prefix="/api",
    tags=["Exportação"],
    dependencies=[Depends(get_current_user)])


@router.get("/exportacao/{year}/{tipo_exportacao}", response_model=ScrapingResponse, summary="Consultar Exportação por ano e por tipo")
async def route_get_exportacao(year: int = datetime.now().year, tipo_exportacao: str = None,  current_user: dict = Depends(get_current_user)):
    """
    Rota para obter os dados de exportação de derivados de uva do Rio Grande do Sul por ano e tipo de produto.

    Esta rota é **protegida** e requer um token JWT válido no header da requisição.

    As categorias disponíveis são:
    - `vinhos_de_mesa`
    - `espumantes`
    - `uvas_frescas`
    - `suco_de_uva`

    ### Parâmetros:
    - `ano`: Ano da consulta (obrigatório)
    - `categoria`: Tipo de produto exportado (obrigatório)

    ### Exemplo de requisição com `curl`:

    ```bash
    curl -X GET "http://localhost:8000/api/exportacao/2022?categoria=espumantes" \
        -H "Authorization: Bearer <seu_token>"
    """
    def get_url(year: int, tipo_exportacao: str):
        dict_sub_opcao = {
            "vinhos_de_mesa": "subopt_01",
            "espumantes": "subopt_02",
            "uvas_frescas": "subopt_03",
            "uvas_passas": "subopt_04",
            "suco_uva": "subopt_05"
        }
        sub_opcao = dict_sub_opcao.get(tipo_exportacao.lower())
        if not sub_opcao:
            raise HTTPException(status_code=400, detail="Tipo de exportação inválido.")
        if not valid_is_int(year):
            raise HTTPException(status_code=400, detail="Ano inválido.")
        return f"/index.php?opcao=opt_06&subopcao={sub_opcao}&ano={year}"

    url = get_url(year, tipo_exportacao)
    scraper = ExportacaoScraper()
    try:
        return ScrapingResponse(status="success", data=scraper.get_content(url), source="live")
    except Exception:
        try:
            return ScrapingResponse(status="success", data=scraper.get_cached_content(url), source="cache")
        except Exception as e_cache:
            raise HTTPException(status_code=500, detail=str(e_cache))
