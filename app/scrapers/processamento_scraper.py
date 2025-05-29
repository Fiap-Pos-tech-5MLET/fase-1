from app.scrapers.base_scraper import BaseScraper
from app.config import get_settings
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import os
import pandas as pd

settings = get_settings()

class ProcessamentoScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url=settings.BASE_URL,cache_dir=os.path.join(settings.HTML_CACHE_DIR, "processamento"))


    def _html_parse(self, soup: BeautifulSoup) -> Dict[str, Any]:
        table = soup.find('table', {'class': 'tb_base tb_dados'})
        data = []
        current_category = ''
        for row in table.find_all('tr'):
            cells = row.find_all(['tr', 'td'])

            if len(cells) != 2:  # Pegando apenas linhas com duas células para evitar erros
                continue

            product_cell, quantity_cell = cells
                # Identifica o tipo do item, se cabeçalho ou itens
            if 'tb_item' in product_cell.get('class', []) or 'tb_subitem' in product_cell.get('class', []):
                current_category = product_cell.get_text(strip=True) if 'tb_item' in product_cell.get('class', []) else current_category
                data.append({
                    'categoria': current_category,
                    'subcategoria': product_cell.get_text(strip=True) if  'tb_subitem' in product_cell.get('class', []) else '-',
                    'quantidade': quantity_cell.get_text(strip=True)
                })
        return self._data_to_dict(data)