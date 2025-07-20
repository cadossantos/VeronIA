from dataclasses import dataclass, field
from typing import List

@dataclass
class SmartWikiPage:
    """Representa uma página da SmartWiki com seus elementos essenciais."""

    url: str                        # URL original da página
    title: str                      # Título da página (extraído do <h1>)
    content: str                    # Conteúdo principal da página, limpo
    links: List[str] = field(default_factory=list)  # Links internos válidos encontrados
