from functools import lru_cache

from core.config_manager import API_ACESSORIES_URL
from core.models import Accessory, AccessoryCheckout

from .base_api_client import BaseAPIClient


class AccessoriesClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=API_ACESSORIES_URL)

    @lru_cache(maxsize=1)  # noqa: B019
    def get_all(self) -> list[Accessory]:
        response_data = self._get(self.base_url)
        return [Accessory(**row) for row in response_data.get("rows", [])]

    @lru_cache(maxsize=512)  # noqa: B019
    def get_checkouts(self, accessory_id: int) -> list[AccessoryCheckout]:
        endpoint = f"{self.base_url}/{accessory_id}/checkedout"
        response_data = self._get(endpoint)
        return [AccessoryCheckout(**row) for row in response_data.get("rows", [])]
