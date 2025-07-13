import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler.fetcher import HtmlFetcher
from crawler.parser import WikiParser
from crawler.storage import PageStorage
from crawler.category_fetcher import CategoryFetcher

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/home/claudiodossantos/dev/projetos/minimo/logs/execution.log"),
        logging.StreamHandler()
    ]
)

def main():
    base_url = "https://wiki.smartsimple.com"
    api_url = "https://wiki.smartsimple.com/api.php"
    category = "Custom_Fields"

    logging.info(f"Iniciando extração da categoria: {category}")

    # Instancia os componentes
    fetcher = HtmlFetcher()
    parser = WikiParser(base_url)
    storage = PageStorage(output_dir="/home/claudiodossantos/dev/projetos/minimo/data/pages")
    cat_fetcher = CategoryFetcher(api_url)

    # Recupera páginas da categoria
    titles = cat_fetcher.get_pages_from_category(category)
    urls = cat_fetcher.build_full_urls(titles, base_url)

    logging.info(f"{len(urls)} páginas encontradas para a categoria '{category}'")

    for i, url in enumerate(urls, 1):
        logging.info(f"[{i}/{len(urls)}] Processando: {url}")
        html = fetcher.get_html(url)
        if not html:
            logging.warning(f"Página pulada (sem HTML): {url}")
            continue
        try:
            page = parser.parse(url, html)
            storage.save_page(page)
        except Exception as e:
            logging.error(f"Erro ao processar página {url}: {e}")

if __name__ == "__main__":
    main()
