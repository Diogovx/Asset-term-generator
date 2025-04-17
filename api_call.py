import requests


class Asset:
    def __init__(self, asset_tag, model, category):
        self.asset_tag = asset_tag
        self.model = model
        self.category = category
        

class User:
    def __init__(self, name, employee_number):
        self.name = name
        self.employee_number = employee_number


def hardwareApiCall(assignedTo):    
    url = f'http://10.1.0.251:8081/api/v1/hardware'
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMDAzNWU2NmYzNjFiNWE0YmY0MWIyNDYzZDBhOWJlNzM4ODQyMmRiYmUwNWRlODdhNGNjMDdkM2QyMTA0ZTgwNGQ0NWZlNTRiY2EyMDFlZTkiLCJpYXQiOjE3NDE2MjcwNzcuMjI0NTg0LCJuYmYiOjE3NDE2MjcwNzcuMjI0NTg3LCJleHAiOjIyMTUwMTI2NzcuMjE0ODY5LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.rfY9gfYj9dEkYpGPvdrQFvSwbnJaLV9LSBMBf49RI8tMGQcCn5e-7jhpjJKAckUSM5txCEtFrr7h2-jS5SOf9Ba5x5DFYdruRudGlqeUVeCISz1HRbY1IaUvCmDw24ZZJ5a_vsPggfJDwVUd94S0bmCTJSm4R1E-oh-D-p9I9P4ikGbC_U-zfc3Bb6ewTshl_EDVAcY2i1z0xbyI9mdvsVM2kQdwELzwH6hxXrLl543Ie8IwAtwlCYXY6B8DWglZFzpvqtVYKklRGIl33zOpq1wuqw5pjMbGE4wnrEBVhK-3s9Hpcu4hsEUuHJj7_1mKZHN4sSf64vC8Xyl0xOijxm-F639Ojlq2-1f6QQysRW1aMq7ghh9iInu8MfyZv7YMIJPN1qXZy81CgzH_jgZXxyeH0-9Pv58jmfY9SMiclp9kPT-ig1gr3CVww82bh4CDVsG8UepcJ7dCpoGNWHHe0F5UJxTTRiri6v6uefM1f8MNooHJFpPxdpGRldNN9tQdtMO8wtNwzIaIhV3OW0GI1utUD0d6ksAE1vvD7wF-T1Gh2P9rEkR7dIFgRQfU5Ds5odPi2f3TjH4wLyQpIQlxy98XFjpKjP3-DXdAKoBqnWs574AbhJMrE1Qfn1ebkHkTH579dOV7WwZxcehcb8Ouzjac9CjNe_O9PLmQMDPUUoI'
            ,'Accept': 'application/json'}
    response = requests.get(url, headers=headers)

    jsonData = response.json()['rows']
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

                userData = User(u['name'], u['employee_number'])
                #asset.append(assetData)
                #asset.append(userData)
        
    #print(user_id)
    data = {
        "assets": assetData,
        "employee_number": userData.employee_number,
        "user_name": userData.name
    }
    if not foundUser:
        print("Usuário não encontrado")
    return data
