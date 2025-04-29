import requests
import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

logger = logging.getLogger(__name__)

class AccessoriesClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    def get_all_accessories(self) -> Dict[str, Any]:
        """ Get the accessories list """
        endpoint = f"{self.base_url}"
        headers = {'Authorization': api_key
                   ,'Accept': 'application/json'}
        
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
    def get_specific_user_accessory(self, user_id):
        """ Get the user's accessories list """
        endpoint = f"{self.base_url}"
        headers = {'Authorization': api_key
                   ,'Accept': 'application/json'}
        
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
        