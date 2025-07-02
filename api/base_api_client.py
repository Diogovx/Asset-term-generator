import logging
from typing import Any

import requests

# import requests_cache
from dotenv import load_dotenv

from core.config_manager import API_KEY

# session = requests_cache.install_cache("snipeit_cache", expire_after=100, backend="sqlite")
load_dotenv()

logger = logging.getLogger(__name__)


class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.api_key: str | None = API_KEY
        if not self.api_key:
            raise ValueError("API_KEY not set in .env")

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
                logger.error(f"Falha ao decodificar JSON da API para '{endpoint}'.")
                return {}

        except requests.exceptions.RequestException as e:
            logger.error(f"API error: {e}")
            raise
