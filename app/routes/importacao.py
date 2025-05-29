from fastapi import APIRouter, HTTPException, Depends
from app.models.responses import ScrapingResponse
from app.scrapers.importacao_scraper import ImportacaoScraper
from app.utils.helpers import valid_is_int
from app.auth.schemas.dependencies import get_current_user  # ← AUTENTICAÇÃO
from datetime import datetime

router = APIRouter(
    prefix="/api",
    tags=["Importação"],
    dependencies=[Depends(get_current_user)])


@router.get("/importacao/{ano}/{tipo_importacao}", response_model=ScrapingResponse, summary="Consultar Importação por ano e por tipo")
async def route_get_importacoes(
    ano: int = datetime.now().year,
    tipo_importacao: str = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Rota para obter os dados de importação de derivados de uva do Rio Grande do Sul por ano e tipo de produto.

    Esta rota é **protegida** e requer um token JWT válido no header da requisição.

    As categorias disponíveis são:
    - `vinhos_de_mesa`
    - `espumantes`
    - `uvas_frescas`
    - `uvas_passas`
    - `suco_de_uva`

    ### Parâmetros:
    - `ano`: Ano da consulta (obrigatório)
    - `tipo_importacao`: Tipo de produto importado (obrigatório)

    ### Exemplo de requisição com `curl`:

    ```bash
    curl -X GET "http://localhost:8000/api/importacao/2023/vinhos_de_mesa" \
        -H "Authorization: Bearer <seu_token>"

    """
    def get_url(year: int, tipo_importacao: str):
        dict_sub_opcao = {
            "vinhos_de_mesa": "subopt_01",
            "espumantes":     "subopt_02",
            "uvas_frescas":   "subopt_03",
            "uvas_passas":    "subopt_04",
            "suco_de_uva":    "subopt_05",
        }
        sub_opcao = dict_sub_opcao.get(tipo_importacao.lower())
        if not sub_opcao:
            raise HTTPException(status_code=400, detail="Tipo de importação inválido.")
        if not valid_is_int(year):
            raise HTTPException(status_code=400, detail="Ano inválido.")
        return f"/index.php?opcao=opt_05&subopcao={sub_opcao}&ano={year}"

    url = get_url(ano, tipo_importacao)
    scraper = ImportacaoScraper()

    try:
        data = scraper.get_content(url)
        return ScrapingResponse(status="success", data=data, source="live")
    except Exception:
        try:
            cached = scraper.get_cached_content(url)
            return ScrapingResponse(status="success", data=cached, source="cache")
        except Exception as e_cache:
            raise HTTPException(status_code=500, detail=str(e_cache))