import logging

from core.models import Asset, User
from util import AssetNotFoundError, UserNotFoundError

from .accessories_client import AccessoriesClient
from .components_client import ComponentsClient

# from util.exceptions import UserNotFoundError, AssetNotFoundError
from .user_api_client import UserClient

logger = logging.getLogger(__name__)

users_client = UserClient()
accessories_client = AccessoriesClient()
components_client = ComponentsClient()


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

    user_asset_ids = {asset.id for asset in assets}

    user_accessories = users_client.get_accessories(user.id)

    all_accessories = accessories_client.get_all()
    for accessory in all_accessories:
        # Para cada acessório do sistema, vemos seu histórico de checkout
        checkouts = accessories_client.get_checkouts(accessory.id)
        for checkout in checkouts:
            # Se o checkout foi para um ativo, e esse ativo é um dos nossos...
            if checkout.assigned_to.type == "asset" and checkout.assigned_to.id in user_asset_ids:
                # Adicionamos o acessório ao ativo correspondente
                for asset in assets:
                    if asset.id == checkout.assigned_to.id:
                        asset.accessories.append(accessory)
                        break

    all_components = components_client.get_all()
    for component in all_components:
        # Para cada componente do sistema, vemos a quais ativos ele pertence
        assignments = components_client.get_assigned_assets(component.id)
        for assignment in assignments:
            # Se o ativo ao qual ele pertence é um dos nossos, adicionamos
            if assignment.id in user_asset_ids:
                # Encontra o objeto Asset correspondente e adiciona o componente
                for asset in assets:
                    if asset.id == assignment.id:
                        asset.components.append(component)
                        break

    for asset in assets:
        asset.accessories.extend(user_accessories)
        # Remove duplicatas se um acessório foi contado duas vezes
        unique_accessories = {acc.id: acc for acc in asset.accessories}.values()
        asset.accessories = list(unique_accessories)

    return user, assets
