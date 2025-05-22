from fastapi import APIRouter, Depends, HTTPException
from app.models.responses import ScrapingResponse
from app.scrapers.comercializacao_scraper import ComercializacaoScraper
from app.auth.schemas.dependencies import get_current_user  # ← AUTENTICAÇÃO

router = APIRouter(
    prefix="/api",
    tags=["Comercialização"],
    dependencies=[Depends(get_current_user)])


#@router.get("/comercializacao", response_model=ScrapingResponse)
#async def route_get_comercializacao(current_user: dict = Depends(get_current_user)):
 #   """
  #  Rota para obter a comercialização de produtos do último ano disponível.
  #  Requer autenticação JWT.
   # """
   # return get_comercializacao(None)


@router.get("/comercializacao/{year}", 
            response_model=ScrapingResponse, 
            summary="Consultar Comercialização por ano")

async def route_get_comercializacao(year: int, current_user: dict = Depends(get_current_user)):
    """
    Rota para obter os dados de comercialização de vinhos e derivados no Rio Grande do Sul por ano.

    Esta rota é **protegida** e requer um token JWT válido no header da requisição.

    Passe o ano como parâmetro no final da URL.

    ### Exemplo de requisição com `curl`:

    ```bash
    curl -X GET "http://localhost:8000/api/comercializacao/2022" \
        -H "Authorization: Bearer <seu_token>"

    """
    return get_comercializacao(year)


def get_comercializacao(year: int):
    """
    Obtém os dados de comercialização de produtos por ano.
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
