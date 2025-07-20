import os
import json
import re
from pathlib import Path
from services.crawler.models import SmartWikiPage
import logging

logger = logging.getLogger(__name__)

class PageStorage:
    """Classe responsável por salvar objetos SmartWikiPage como arquivos .json no disco."""

    def __init__(self, output_dir: str = "data/pages"):
        # Define diretório padrão de saída (pasta 'data/pages')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir

    def sanitize_filename(self, title: str) -> str:
        """Remove caracteres inválidos para criação de nomes de arquivo."""
        title = title.lower().strip().replace(" ", "_")
        return re.sub(r'[^a-zA-Z0-9_-]', '', title)

    def save_page(self, page: SmartWikiPage):
        """Salva o conteúdo de uma SmartWikiPage como arquivo .json."""
        filename = self.sanitize_filename(page.title) or "untitled"
        filepath = self.output_dir / f"{filename}.json"

        # Cria o dicionário que será salvo
        page_data = {
            "url": page.url,
            "title": page.title,
            "content": page.content,
            "links": page.links,
            "images": getattr(page, "images", [])
        }


        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(page_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Página salva em: {filepath}")
        except Exception as e:
            logger.error(f"Falha ao salvar página '{page.title}': {e}")
