from core.config_manager import API_COMPONENTS_URL
from core.models import Component

from .base_api_client import BaseAPIClient


class ComponentsClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=API_COMPONENTS_URL)

    def get_all_components(self) -> list[Component]:
        """Get all components list"""
        response_data = self._get(self.base_url)

        return [Component(**row) for row in response_data.get("rows", [])]
