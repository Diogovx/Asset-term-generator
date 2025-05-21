import logging

from dotenv import load_dotenv

import api
from core.config_manager import API_ACESSORIES_URL, API_HARDWARE_URL, API_USERS_URL

load_dotenv()
logger = logging.getLogger(__name__)

def get_api_url():
    return {
        "hardware": API_HARDWARE_URL,
        "users": API_USERS_URL,
        "accessories": API_ACESSORIES_URL
    }

def hardware_api_call(assigned_to):  
    try:
        client = api.HardwareClient(base_url=get_api_url().get('hardware', ''))
        response = client.get_assets_by_employee()
        assets_response = response['rows']
    
        found_user = False
        user_data = None
        asset_data = []
        for _i, asset_item in enumerate(assets_response):
            assigned_user = asset_item.get('assigned_to', '')
            if assigned_user is not None:
                if assigned_user.get('employee_number', '') == assigned_to:
                    found_user = True

                    asset_data.append(
                                    {
                                        "asset_id": asset_item.get('id', ''),
                                        "asset_tag": asset_item.get('asset_tag', ''),
                                        "serial": asset_item.get('serial', ''),
                                        "model": asset_item.get('model', '').get('name', ''),
                                        "category": asset_item.get('category', '').get('name', '')
                                    }
                                )

                    user_data = {
                            "user_id": assigned_user.get('id', ''),
                            "user_name": assigned_user.get('name', ''),
                            "employee_number": assigned_user.get('employee_number', '')
                        }
        
        if not found_user:
            logger.info(f"Usuário com matrícula {assigned_to} não encontrado")
            return {
                "assets": [],
                "employee_number": assigned_to,
                "user_name": "NÃO ENCONTRADO"
            }
        return {
            "assets": asset_data,
            "user_id": user_data.get('user_id', ''),
            "user_name": user_data.get('user_name', ''),
            "employee_number": user_data.get('employee_number', '')
        }
    except Exception as e:
        logger.error(f"Erro na chamada da API: {e}")
        return {
            "assets": [],
            "employee_number": assigned_to,
            "user_name": "ERRO NA CONSULTA"
        }


def accessories_api_call(id, user_has_accessories = True):
    
    if not user_has_accessories:
        client = api.AccessoriesClient(base_url=str(get_api_url().get('accessories', '')))
        response = client.get_user_accessory()
        accessories_response = response['rows']
        return accessories_response
    client = api.AccessoriesClient(
        base_url=str(get_api_url().get('users', '')) + f'/{id}/accessories'
    )
    response = client.get_user_accessory()
    accessories_response = response['rows']
    
    return accessories_response

def specific_api_call(accessory_id):
    client = api.AccessoriesClient(
        base_url=str(get_api_url().get('accessories', '')) + f'{accessory_id}/checkedout'
    )
    response = client.get_user_accessory()
    accessories_response = response['rows']
    return accessories_response

def has_multiple_assets(filtered_assets):
    if len(filtered_assets) > 1:
        return True
    else:
        return False