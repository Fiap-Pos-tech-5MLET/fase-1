from app.scrapers.base_scraper import BaseScraper
from app.config import get_settings
from bs4 import BeautifulSoup
from typing import Dict, Any
import os

settings = get_settings()

class ExportacaoScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url=settings.BASE_URL, cache_dir=os.path.join(settings.HTML_CACHE_DIR, "exportacao"))

    def _html_parse(self, soup: BeautifulSoup) -> Dict[str, Any]:
        table = soup.find('table', {'class': 'tb_base tb_dados'})
        data = []

        for row in table.find_all('tr'):
            cells = row.find_all(['td'])

            # Esperamos exatamente 3 colunas: país, quantidade, valor
            if len(cells) != 3:
                continue

            pais_cell, quantidade_cell, valor_cell = cells

            data.append({
                'categoria': '-',  # Padrão usado quando não há categoria
                'subcategoria': pais_cell.get_text(strip=True),  # Aqui 'pais' vira 'subcategoria'
                'quantidade': quantidade_cell.get_text(strip=True),
                'valor': valor_cell.get_text(strip=True)
            })

        return self._data_to_dict(data)
