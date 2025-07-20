import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from services.crawler.models import SmartWikiPage

class WikiParser:
    """Responsável por extrair o conteúdo e metadados de uma página da SmartWiki."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse(self, url: str, html: str) -> SmartWikiPage:
        soup = BeautifulSoup(html, "lxml")

        # Extrai título da página
        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Sem título"

        # Localiza o conteúdo principal da página
        content_div = soup.find("div", {"id": "bodyContent"})
        raw_content = content_div.get_text(separator="\n").strip() if content_div else "Sem conteúdo"
        content = re.sub(r'\t+', ' ', raw_content)       # Remove tabs
        content = re.sub(r'\n{2,}', '\n', content)        # Reduz múltiplas quebras de linha
        content = re.sub(r' {2,}', ' ', content)          # Reduz múltiplos espaços

        # Extrai links internos
        raw_links = content_div.find_all("a", href=True) if content_div else []
        links = [
            urljoin(self.base_url, a["href"])
            for a in raw_links
            if a["href"].startswith("/wiki/") and ":" not in a["href"]
        ]

        # Extrai imagens (atributos src absolutos)
        raw_images = content_div.find_all("img", src=True) if content_div else []
        images = [
            urljoin(self.base_url, img["src"])
            for img in raw_images
        ]

        # Adiciona campo opcional de imagens ao modelo
        page = SmartWikiPage(
            url=url,
            title=title,
            content=content,
            links=links,
        )

        # 🔧 Adiciona dinamicamente se quiser já suportar isso
        setattr(page, "images", images)

        return page
