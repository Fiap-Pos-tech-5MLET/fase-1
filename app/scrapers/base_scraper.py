import requests
import os
import hashlib
import pandas as pd
from abc import ABC
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from app.utils.helpers import clean_quantity

class BaseScraper(ABC):
    def __init__(self, base_url: str, cache_dir: str):
        self.base_url = base_url
        self.cache_dir = cache_dir

        os.makedirs(cache_dir, exist_ok=True)

    def parse_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        # Verifica se possui dados para efetuar o parse
        return self._html_parse(soup) if self._is_parsed(soup) else "O html não pode ser parseado"

    def _is_parsed(self, soup: BeautifulSoup) -> bool:
        """Verifica se possui dados a serem extraidos"""
        return soup.find('table', {'class': 'tb_base tb_dados'}) is not None

    def get_content(self, endpoint: str = "") -> Dict[str, Any]:
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Gera o nome do arquivo (md5) com base no endpoint
            filename = self._generate_filename(endpoint)

            # salva o html na pasta para consultas
            with open(os.path.join(self.cache_dir, filename), 'w', encoding='utf-8') as file:
                file.write(response.text)

            soup = BeautifulSoup(response.text, 'html.parser')
            return self.parse_content(soup)
        except requests.RequestException:
            # Fallback para HTML local
            return self.get_cached_content(endpoint)

    def get_cached_content(self, endpoint: str) -> Dict[str, Any]:
        # Gera o nome do arquivo (md5) com base no endpoint
        filename = self._generate_filename(endpoint)

        cache_file = os.path.join(self.cache_dir, filename)
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                return self.parse_content(soup)
        else:
            raise Exception("Conteúdo não disponível em cache")

    def _generate_filename(self, endpoint: str) -> str:
        return f"{hashlib.md5(endpoint.encode()).hexdigest()}.html"

    def _data_to_dict(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Converte os dados extraídos para um dicionário,
        aplicando limpeza nas colunas 'quantidade' e 'valor' se existirem.
        """
        df = pd.DataFrame(data)

        if 'quantidade' in df.columns:
            df['quantidade'] = df['quantidade'].apply(clean_quantity)

        if 'valor' in df.columns:
            df['valor'] = df['valor'].apply(clean_quantity)

        return df.to_dict(orient='records')
