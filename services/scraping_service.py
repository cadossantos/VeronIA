import os
import logging
from urllib.parse import urlparse
from smartwiki.crawler.fetcher import HtmlFetcher
from smartwiki.crawler.parser import WikiParser
from smartwiki.crawler.storage import PageStorage
from smartwiki.crawler.category_fetcher import CategoryFetcher # Importar CategoryFetcher
from smartwiki.rag.ingest import ingest_from_directory

logging.basicConfig(level=logging.INFO)

class ScrapingService:
    """Serviço para orquestrar o scraping e a ingestão de dados para o RAG."""

    def __init__(self):
        self.fetcher = HtmlFetcher()

    def scrape_and_ingest_website(self, url: str, collection_name: str) -> dict:
        """
        Realiza o scraping de uma URL, salva os dados e os ingere no Vector Store.

        Args:
            url (str): A URL inicial para o scraping.
            collection_name (str): O nome da coleção para o Vector Store.

        Returns:
            dict: Um dicionário com o resultado da operação.
        """
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return {"success": False, "error": "URL inválida. Certifique-se de incluir o esquema (ex: https://)."}
            
            # Define o base_url para o WikiParser com base no domínio da URL fornecida
            base_url_for_parser = f"{parsed_url.scheme}://{parsed_url.netloc}"
            self.parser = WikiParser(base_url=base_url_for_parser)

            # Define um diretório de saída específico para esta coleção
            output_dir = os.path.join("smartwiki", "data", "pages", collection_name)
            storage = PageStorage(output_dir=output_dir)
            os.makedirs(output_dir, exist_ok=True) # Garante que o diretório exista

            logging.info(f"[ScrapingService] Iniciando scraping da URL: {url}")
            html = self.fetcher.get_html(url)
            if not html:
                logging.error(f"[ScrapingService] Falha ao obter HTML da URL: {url}")
                return {"success": False, "error": f"Falha ao obter HTML da URL: {url}"}

            logging.info(f"[ScrapingService] HTML obtido. Iniciando parsing da URL: {url}")
            page = self.parser.parse(url, html)
            storage.save_page(page)
            logging.info(f"[ScrapingService] Página salva em: {output_dir}")

            logging.info(f"[ScrapingService] Iniciando ingestão para a coleção: {collection_name}")
            ingest_from_directory(data_dir=output_dir, vector_store_dir="smartwiki/data/vector_store", collection_name=collection_name)
            logging.info(f"[ScrapingService] Ingestão para a coleção '{collection_name}' concluída.")
            
            return {"success": True, "files_processed": 1, "collection": collection_name}

        except Exception as e:
            logging.error(f"[ScrapingService] Erro durante o scraping e ingestão: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def scrape_and_ingest_category(self, api_url: str, category_name: str, collection_name: str) -> dict:
        """
        Realiza o scraping de todas as páginas de uma categoria MediaWiki e as ingere.
        """
        try:
            category_fetcher = CategoryFetcher(api_url)
            titles = category_fetcher.get_pages_from_category(category_name)
            
            if not titles:
                return {"success": False, "error": f"Nenhuma página encontrada para a categoria '{category_name}'."}

            # Extrai o base_url do api_url para construir as URLs completas das páginas
            parsed_api_url = urlparse(api_url)
            base_url_for_pages = f"{parsed_api_url.scheme}://{parsed_api_url.netloc}"

            urls = category_fetcher.build_full_urls(titles, base_url_for_pages)
            
            total_files_processed = 0
            for i, url in enumerate(urls):
                logging.info(f"[ScrapingService] Processando página {i+1}/{len(urls)} da categoria: {url}")
                result = self.scrape_and_ingest_website(url, collection_name) # Reutiliza a função de página única
                if result.get("success"):
                    total_files_processed += 1
                else:
                    logging.warning(f"[ScrapingService] Falha ao processar URL da categoria {url}: {result.get('error')}")
            
            if total_files_processed == 0:
                return {"success": False, "error": "Nenhuma página da categoria foi processada com sucesso."}

            return {"success": True, "files_processed": total_files_processed, "collection": collection_name}

        except Exception as e:
            logging.error(f"[ScrapingService] Erro durante o scraping da categoria: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
