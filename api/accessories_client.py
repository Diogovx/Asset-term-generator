from typing import Any

from .base_api_client import BaseAPIClient


class AccessoriesClient(BaseAPIClient):
    def get_user_accessory(self) -> dict[str, Any]:
        """Get the user's accessories list"""
        return self._get(self.base_url)
