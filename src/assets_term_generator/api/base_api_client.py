import logging
from typing import Any

import requests
from dotenv import load_dotenv
from rich.console import Console

from assets_term_generator.core.config_manager import API_KEY

load_dotenv()

logger = logging.getLogger(__name__)
console = Console()


class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.api_key: str | None = API_KEY

    def _get(self, endpoint: str) -> dict[str, Any]:
        headers: dict[str, Any] = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            response.raise_for_status()

            if not response.text or not response.content:
                logger.warning(f"Resposta da API para '{endpoint}' veio com corpo vazio.")
                return {}

            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                console.print(
                    "[bold red]API ERROR[/bold red]:"
                    f"Falha ao decodificar JSON da API para '{endpoint}'."
                )
                logger.exception(f"Failed to decode API JSON for '{endpoint}'")
                return {}

        except requests.exceptions.RequestException:
            console.print("[bold red]API ERROR[/bold red]: Erro na requisição")
            logger.exception("An error occurred in the request")
            raise
