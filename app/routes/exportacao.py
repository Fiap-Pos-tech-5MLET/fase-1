from fastapi import APIRouter, HTTPException
from app.auth.bearer import BearerAuth
from app.models.responses import ScrapingResponse
from app.scrapers.exportacao_scraper import ExportacaoScraper
from app.utils.helpers import valid_is_int
from datetime import datetime

router = APIRouter(prefix="/api")
bearer_auth = BearerAuth()

@router.get("/exportacao/{year}/{tipo_exportacao}", response_model=ScrapingResponse)
async def route_get_exportacao(year: int = datetime.now().year, tipo_exportacao: str = None):
    """
    Rota para obter a exportação de derivados de uva por ano e tipo.
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
