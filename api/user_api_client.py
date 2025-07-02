from core.config_manager import API_USERS_URL
from core.models import Accessory, Asset, Component, User, UserAssetsResponse, UserSearchResponse

from .base_api_client import BaseAPIClient


# TODO User client API
class UserClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=API_USERS_URL)

    def find_by_employee_number(self, employee_number: str) -> User | None:
        endpoint = f"{self.base_url}?employee_num={employee_number}"
        response_data = self._get(endpoint)
        parsed_response = UserSearchResponse(**response_data)

        return parsed_response.rows[0] if parsed_response.rows else None

    def get_assets(self, user_id: int) -> list[Asset]:
        endpoint = f"{self.base_url}/{user_id}/assets"
        response_data = self._get(endpoint)

        parsed_response = UserAssetsResponse(**response_data)
        return parsed_response.rows

    def get_accessories(self, user_id: int) -> list[Accessory]:
        endpoint = f"{self.base_url}/{user_id}/accessories"
        response_data = self._get(endpoint)

        return [Accessory(**row) for row in response_data.get("rows", [])]

    def get_components(self, user_id: int) -> list[Component]:
        endpoint = f"{self.base_url}/{user_id}/components"
        response_data = self._get(endpoint)

        return [Component(**row) for row in response_data.get("rows", [])]
