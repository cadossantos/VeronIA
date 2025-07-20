import requests
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)

class CategoryFetcher:
    """Consulta a API do MediaWiki e retorna todas as páginas de uma categoria."""

    def __init__(self, api_url: str):
        # Exemplo: "https://wiki.smartsimple.com/api.php"
        self.api_url = api_url

    def get_pages_from_category(self, category_name: str, limit: int = 500) -> list:
        """
        Recupera os títulos das páginas de uma categoria da wiki.
        
        Args:
            category_name (str): Nome da categoria (ex: "Custom_Fields").
            limit (int): Máximo de páginas por chamada (padrão 500).

        Returns:
            list[str]: Lista com títulos das páginas.
        """
        all_pages = []
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category_name}",
            "format": "json",
            "cmlimit": limit,
        }

        while True:
            response = requests.get(self.api_url, params=params)
            if response.status_code != 200:
                logger.error(f"Falha ao acessar API: {response.status_code}")
                break

            data = response.json()
            members = data.get("query", {}).get("categorymembers", [])
            all_pages.extend([m["title"] for m in members])

            # Verifica se há continuação (mais páginas a buscar)
            if "continue" in data:
                params.update(data["continue"])
            else:
                break

        return all_pages

    def build_full_urls(self, titles: list[str], base_url: str) -> list:
        """Recebe títulos e constrói URLs completas para cada página."""
        return [f"{base_url}/wiki/{quote(title.replace(' ', '_'))}" for title in titles]