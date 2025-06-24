from typing import Any

from .base_api_client import BaseAPIClient


class HardwareClient(BaseAPIClient):
    def get_assets_by_employee(self) -> dict[str, Any]:
        """Get employee's equipaments"""
        return self._get(self.base_url)
