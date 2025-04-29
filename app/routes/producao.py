from fastapi import APIRouter, Depends, HTTPException
from app.auth.bearer import BearerAuth
from app.models.responses import ScrapingResponse
from app.scrapers.producao_scraper import ProducaoScraper

router = APIRouter(prefix="/api")
bearer_auth = BearerAuth()

@router.get("/producao", response_model=ScrapingResponse)
async def route_get_producao():
    """
    Rota para obter a produção de produtos do ultimo ano disponivel.
    """
    
    return get_producao(None)


@router.get("/producao/{year}", response_model=ScrapingResponse)
# async def get_produtos(token: str = Depends(bearer_auth)):
async def route_get_producao_by_year(year: int):
    return get_producao(year)


def get_producao(year: int):
    """
    Obtem os dados de produção de produtos por ano.
    """
    try:
        scraper = ProducaoScraper()

        # if True:
        #     raise Exception("Forçando cair no exception")

        data = scraper.get_content("/index.php?opcao=opt_02" + (f"&ano={year}" if year else ""))


        return ScrapingResponse(
            status="success",
            data=data,
            source="live"
        )
    except Exception as e:
        try:
            cached_data = scraper.get_cached_content("/index.php?opcao=opt_02" + (f"&ano={year}" if year else ""))
            return ScrapingResponse(
                status="success",
                data=cached_data,
                source="cache"
            )
        except Exception as e_cache:
            raise HTTPException(status_code=500, detail=str(e_cache))
