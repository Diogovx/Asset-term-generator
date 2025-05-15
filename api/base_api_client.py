from config import API_KEY
import requests
import logging
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.api_key = API_KEY
        if not self.api_key:
            raise ValueError("API_KEY not set in .env")
    
    def _get(self, endpoint: str) -> Dict[str, Any]:
        headers = {
            'Authorization': f'{self.api_key}',
            'Accept': 'application/json'
        }
        try:
            response = requests.get(
                endpoint,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API error: {e}")
            raise
