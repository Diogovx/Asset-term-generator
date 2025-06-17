from typing import Any

from .base_api_client import BaseAPIClient


class ComponentsClient(BaseAPIClient):
    def get_asset_components(self) -> dict[str,Any]:
        """ Get asset's components """
        return self._get(self.base_url)