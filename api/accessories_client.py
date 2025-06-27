from core.config_manager import API_ACESSORIES_URL
from core.models import Accessory

from .base_api_client import BaseAPIClient


class AccessoriesClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=API_ACESSORIES_URL)

    def get_all_accessory(self) -> list[Accessory]:
        """Get all accessories list"""
        response_data = self._get(self.base_url)

        return [Accessory(**row) for row in response_data.get("rows", [])]
