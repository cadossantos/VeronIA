import requests

class HtmlFetcher:
    """Responsável por fazer requisições HTTP e retornar o HTML bruto."""

    def __init__(self, user_agent: str = None):
        # Define um user-agent padrão para simular navegador real
        self.headers = {
            "User-Agent": user_agent or "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
        }

    def get_html(self, url: str) -> str:
        """Faz uma requisição GET à URL e retorna o conteúdo HTML bruto (ou None em caso de erro)."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Levanta exceção para status != 200
            return response.text
        except requests.RequestException as e:
            print(f"[ERRO] Falha ao acessar {url} -> {e}")
            return None
