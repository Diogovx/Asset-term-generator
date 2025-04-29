import os
import api
from dotenv import load_dotenv
from models import User

load_dotenv()

api_hardware_url = os.getenv("API_HARDWARE_URL")
api_users_url = os.getenv("API_USERS_URL")
api_acessories_url = os.getenv("API_ACESSORIES_URL")

def hardwareApiCall(assignedTo):  
    client = api.HardwareClient(base_url=api_hardware_url)
    response = client.get_assets_by_employee()
    jsonData = response['rows']
    assignedTo = assignedTo
    
    
    foundUser = False
    userData = ''
    assetData = []
    for i, v in enumerate(jsonData):
        u = v['assigned_to']
        if u is not None:
            if u['employee_number'] == assignedTo:
                foundUser = True

                assetData.append({"asset_tag": v.get('asset_tag'), "model": v.get('model').get('name'), "category": v.get('category').get('name')})

                userData = User(u['id'] ,u['name'], u['employee_number'])
        
    data = {
        "assets": assetData,
        "user_id": userData.user_id,
        "employee_number": userData.employee_number,
        "user_name": userData.name
    }
    if not foundUser:
        print("Usuário não encontrado")
    return data

# TODO Fazer api de acessórios

def accessoriesApiCall(user_id):
    
    client = api.AccessoriesClient(base_url=str(api_users_url) + f'/{user_id}/accessories')
    response = client.get_specific_user_accessory(user_id)
    jsonData = response['rows']
    
    return jsonData