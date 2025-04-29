from app.scrapers.base_scraper import BaseScraper
from app.config import get_settings
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import os
import pandas as pd
from app.utils.helpers import clean_quantity

settings = get_settings()

class ComercializacaoScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url=settings.BASE_URL,
            cache_dir=os.path.join(settings.HTML_CACHE_DIR, "comercializacao")
        )
    
    def parse_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        # Verifica se possui dados para efetuar o parse
        if self._is_parsed(soup):
            return self._html_parse(soup)
        else:
            raise "O html não pode ser parseado"
    
    def _is_parsed(self, soup: BeautifulSoup) -> bool:
        """Verifica se possui dados a serem extraidos"""
        return soup.find('table', {'class': 'tb_base tb_dados'}) is not None
    
    def _html_parse(self, soup: BeautifulSoup) -> Dict[str, Any]:
        data = []
        
        table = soup.find('table', {'class': 'tb_base tb_dados'})
        # extraindo  as linhas da tabela
        rows = table.find_all('tr')

        for row in table.find_all('tr'):
            cells = row.find_all(['th', 'td'])
            
            if len(cells) == 2:  # Pegando apenas linhas com duas células para evitar erros
                product_cell, quantity_cell = cells
                
                # Identifica o tipo do item, se cabeçalho ou itens
                if 'tb_item' in product_cell.get('class', []):
                    current_category = product_cell.get_text(strip=True)
                    data.append({
                        'categoria': current_category,
                        'subcategoria': '-',
                        'quantidade': quantity_cell.get_text(strip=True)
                    })
                elif 'tb_subitem' in product_cell.get('class', []):
                    data.append({
                        'categoria': current_category,
                        'subcategoria': product_cell.get_text(strip=True),
                        'quantidade': quantity_cell.get_text(strip=True)
                    })
                # elif 'tb_total' in row.find_parent('tfoot').get('class', []):
                else:
                    # Opcional: tratamento para o total
                    pass
        
        #Converte os dados para um dataframe
        df = pd.DataFrame(data)
        df['quantidade'] = df['quantidade'].apply(clean_quantity)
        
        return df.to_dict(orient='records')