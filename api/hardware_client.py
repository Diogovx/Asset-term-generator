from .base_api_client import BaseAPIClient
from typing import Dict, Any

class HardwareClient(BaseAPIClient):
    def get_assets_by_employee(self) -> Dict[str,Any]:
        """ Get employee's equipaments """
        return self._get(self.base_url)