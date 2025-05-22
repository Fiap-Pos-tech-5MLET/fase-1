from fastapi import APIRouter, Depends, HTTPException
from app.models.responses import ScrapingResponse
from app.scrapers.producao_scraper import ProducaoScraper
from app.auth.schemas.dependencies import get_current_user  # Autenticação com JWT

router = APIRouter(
    prefix="/api",
    tags=["Produção"],
    dependencies=[Depends(get_current_user)])

#@router.get("/producao", response_model=ScrapingResponse, responses={
 #       200: {"description": "Dados de produção retornados com sucesso"},
  #      401: {"description": "Token JWT ausente ou inválido"},
   
   #     500: {"description": "Erro ao processar os dados"}
 #   },
   # summary="Consultar pordução por ano")
#async def route_get_producao(current_user: dict = Depends(get_current_user)):
    #"""
    #Rota para obter a produção de produtos do último ano disponível. \n
    #Requer autenticação JWT. \n
    #Para consultar um ano específico, use a rota com filtro de ano
    #"""
    #return get_producao(None)

@router.get("/producao/{year}", response_model=ScrapingResponse, responses={
        200: {"description": "Dados de produção retornados com sucesso"},
        401: {"description": "Token JWT ausente ou inválido"},
        404: {"description": "Ano não encontrado ou dados indisponíveis"},
        500: {"description": "Erro ao processar os dados"}
    },
    summary="Consultar produção por ano")

async def route_get_producao_by_year(year: int, current_user: dict = Depends(get_current_user)):
    """
    Rota para obter a produção de vinhos, sucos e derivados do Rio Grande do Sul por ano.

    Esta rota é **protegida** e requer um token JWT válido no header da requisição.

    Passe o ano como parâmetro no final da URL.

    ### Exemplo de requisição com `curl`:

    ```bash
    curl -X GET "http://localhost:8000/api/producao/2022" \
        -H "Authorization: Bearer <seu_token>"
"""
    return get_producao(year)

def get_producao(year: int):
    """
    Obtém os dados de produção de produtos por ano.
    """
      
    try:
        scraper = ProducaoScraper()
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