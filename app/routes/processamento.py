from fastapi import APIRouter, HTTPException
from app.auth.bearer import BearerAuth
from app.models.responses import ScrapingResponse
from app.scrapers.processamento_scraper import ProcessamentoScraper
from app.utils.helpers import valid_is_int
from datetime import datetime

router = APIRouter(prefix="/api")
bearer_auth = BearerAuth()

@router.get("/processamento/{year}/{tipo_processamento}", response_model=ScrapingResponse)
async def route_get_producao_by_year(year: int =datetime.now().year,tipo_processamento: str = None):
    """
    Rota para obter a produção de produtos por ano e tipo de processamento.
    """
    def get_url(year: int, tipo_processamento: str):
        """
        Gera a URL para obter os dados de produção de produtos por ano.
        """
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

    url = get_url(year, tipo_processamento)
    scraper = ProcessamentoScraper()
    try:
        return ScrapingResponse(status="success",data=scraper.get_content(url),source="live")
    except Exception as e:
        try:
            return ScrapingResponse(status="success",data=scraper.get_cached_content(url),source="cache")
        except Exception as e_cache:
            raise HTTPException(status_code=500, detail=str(e_cache))