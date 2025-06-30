import logging
from functools import lru_cache

from core.models import Accessory, Asset, Component, User
from util import AssetNotFoundError, UserNotFoundError

from .accessories_client import AccessoriesClient
from .components_client import ComponentsClient

# from util.exceptions import UserNotFoundError, AssetNotFoundError
from .user_api_client import UserClient

logger = logging.getLogger(__name__)

users_client = UserClient()
accessories_client = AccessoriesClient()
components_client = ComponentsClient()


@lru_cache(maxsize=1)
def get_all_accessories() -> list[Accessory]:
    return accessories_client.get_all_accessory()


def get_all_components() -> list[Component]:
    return components_client.get_all_components()


def get_user_and_assets(employee_number: str) -> tuple[User, list[Asset]]:
    """
    Orquestra as chamadas para buscar um usuário e sua lista de ativos já enriquecida.
    Esta é a principal função que será consumida pelo main.py.
    """
    logger.info(f"Buscando usuário com matrícula {employee_number}...")
    user = users_client.find_by_employee_number(employee_number)
    if not user:
        raise UserNotFoundError(f"Usuário com matrícula {employee_number} não encontrado.")

    logger.info(f"Buscando ativos para o usuário '{user.name}'...")
    assets = users_client.get_assets(user.id)
    if not assets:
        raise AssetNotFoundError(f"Nenhum ativo encontrado para o usuário {user.name}.")

    all_accessories = get_all_accessories()
    all_components = get_all_components()

    asset_map = {asset.id: asset for asset in assets}

    for component in all_components:
        asset_id = getattr(component, "assigned_to", None)
        if asset_id in asset_map:
            asset_map[asset_id].components.append(component)

    for accessory in all_accessories:
        asset_id = getattr(accessory, "assigned_to", None)
        if asset_id in asset_map:
            asset_map[asset_id].accessories.append(accessory)

    return user, list(asset_map.values())
