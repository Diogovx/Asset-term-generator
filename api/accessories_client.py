import requests
import os
import logging
from .base_api_client import BaseAPIClient
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

logger = logging.getLogger(__name__)

class AccessoriesClient(BaseAPIClient):
    def get_user_accessory(self):
        """ Get the user's accessories list """
        return self._get(self.base_url)