import logging

from assets_term_generator.models import Asset, User
from assets_term_generator.util import AssetNotFoundError, UserNotFoundError

from .accessories_client import AccessoriesClient
from .components_client import ComponentsClient
from .user_api_client import UserClient

logger = logging.getLogger(__name__)

users_client = UserClient()
accessories_client = AccessoriesClient()
components_client = ComponentsClient()


def get_user_and_assets(employee_number: str) -> tuple[User, list[Asset]]:
    """Orchestrates calls to search for a user

    Args:
        employee_number (str)

    Raises:
        UserNotFoundError
        AssetNotFoundError

    Returns:
        tuple[User, list[Asset]]
    """
    logger.info(f"Buscando usuário com matrícula {employee_number}...")
    user = users_client.find_by_employee_number(employee_number)
    if not user:
        raise UserNotFoundError(employee_number)

    logger.info(f"Buscando ativos para o usuário '{user.name}'...")
    assets = users_client.get_assets(user.id)
    if not assets:
        raise AssetNotFoundError(assets)

    user_asset_ids = {asset.id for asset in assets}

    user_accessories = users_client.get_accessories(user.id)

    all_accessories = accessories_client.get_all()
    for accessory in all_accessories:
        checkouts = accessories_client.get_checkouts(accessory.id)
        for checkout in checkouts:
            if checkout.assigned_to.type == "asset" and checkout.assigned_to.id in user_asset_ids:
                for asset in assets:
                    if asset.id == checkout.assigned_to.id:
                        asset.accessories.append(accessory)
                        break

    all_components = components_client.get_all()
    for component in all_components:
        assignments = components_client.get_assigned_assets(component.id)
        for assignment in assignments:
            if assignment.id in user_asset_ids:
                for asset in assets:
                    if asset.id == assignment.id:
                        asset.components.append(component)
                        break

    for asset in assets:
        asset.accessories.extend(user_accessories)
        unique_accessories = {acc.id: acc for acc in asset.accessories}.values()
        asset.accessories = list(unique_accessories)

    return user, assets
