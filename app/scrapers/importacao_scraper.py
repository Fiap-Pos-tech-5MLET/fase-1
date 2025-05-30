from app.scrapers.base_scraper import BaseScraper
from app.config import get_settings
from bs4 import BeautifulSoup
from typing import Dict, Any
import os

settings = get_settings()

class ImportacaoScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url=settings.BASE_URL,
            cache_dir=os.path.join(settings.HTML_CACHE_DIR, "importacao")
        )

    def _html_parse(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Analisa a página de importações e retorna um dict com:
        - categoria: sempre '-' (sem categoria adicional)
        - subcategoria: país de origem
        - quantidade: texto da 2ª célula
        - valor: texto da 3ª célula
        """

        table = soup.find('table', {'class': 'tb_base tb_dados'})

        texto = soup.find_all('p', {'class':'text_center'})[0].get_text(strip=True)

        # 1) remove tudo até "de " (inclusive)
        parte = texto.split("de ", 1)[1]

        # 2) remove tudo a partir de " [" (inclusive)
        categoria = parte.split(" [", 1)[0]

        data = []
        tbody = table.find('tbody')
        for row in tbody.find_all('tr'):
            cells = row.find_all(['td'])

            # Esperamos exatamente 3 colunas: país, quantidade, valor
            if len(cells) != 3:
                continue

            pais_cell, quantidade_cell, valor_cell = cells

            data.append({
                'categoria': categoria,  
                'pais': pais_cell.get_text(strip=True),  # Aqui 'pais' vira 'subcategoria'
                'quantidade': quantidade_cell.get_text(strip=True),
                'valor': valor_cell.get_text(strip=True)
            })

        return self._data_to_dict(data)
