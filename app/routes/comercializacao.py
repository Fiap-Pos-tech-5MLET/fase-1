from fastapi import APIRouter, Depends, HTTPException
from app.auth.bearer import BearerAuth
from app.models.responses import ScrapingResponse
from app.scrapers.comercializacao_scraper import ComercializacaoScraper
from app.scrapers.producao_scraper import ProducaoScraper

router = APIRouter(prefix="/api")
bearer_auth = BearerAuth()

@router.get("/comercializacao", response_model=ScrapingResponse)
async def route_get_comercializacao():
    """
    Rota para obter a comercialização de produtos do ultimo ano disponivel.
    """
    return get_comercializacao(None)

@router.get("/comercializacao/{year}", response_model=ScrapingResponse)
async def route_get_comercializacao(year: int):
    """
    Rota para obter a comercialização de produtos por ano.
    """
    return get_comercializacao(year)


def get_comercializacao(year: int):
    """
    Obtem os dados de comercialização de produtos por ano.
    """
    try:
        scraper = ComercializacaoScraper()
        data = scraper.get_content("/index.php?opcao=opt_04" + (f"&ano={year}" if year else ""))
        return ScrapingResponse(
            status="success",
            data=data,
            source="live"
        )
    except Exception as e:
        try:
            cached_data = scraper.get_cached_content("/index.php?opcao=opt_04" + (f"&ano={year}" if year else ""))
            return ScrapingResponse(
                status="success",
                data=cached_data,
                source="cache"
            )
        except Exception as e_cache:
            raise HTTPException(status_code=500, detail=str(e_cache))