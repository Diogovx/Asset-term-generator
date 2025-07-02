from functools import lru_cache

from core.config_manager import API_COMPONENTS_URL
from core.models import Component, ComponentAssetAssignment

from .base_api_client import BaseAPIClient


class ComponentsClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=API_COMPONENTS_URL)

    @lru_cache(maxsize=1)  # noqa: B019
    def get_all(self) -> list[Component]:
        """Get all components list"""
        response_data = self._get(self.base_url)

        return [Component(**row) for row in response_data.get("rows", [])]

    @lru_cache(maxsize=512)  # noqa: B019
    def get_assigned_assets(self, component_id: int) -> list[ComponentAssetAssignment]:
        endpoint = f"{self.base_url}/{component_id}/assets"
        response_data = self._get(endpoint)
        return [ComponentAssetAssignment(**row) for row in response_data.get("rows", [])]
