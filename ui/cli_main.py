from InquirerPy import inquirer


class Menu:
    def menu_select_term(self):
        choose = inquirer.select(
            message="Você deseja gerar qual termo?\nEscolha um deles: ",
            choices=[
                {
                    'name': 'Notebook', 'value': 'Laptops',
                },
                {
                    'name': 'Celular', 'value': 'Smartphones',
                }
            ],
            default=None
        ).execute()
        return choose
    def menu_select_asset(self, asset_list, selected_term):
        choose = inquirer.select(
            message="Foi encontrados mais de um ativo do usuário!\nEscolha um deles: ",
            choices=[
            {
                'name': f"{
                    asset.get('asset_tag')
                } - {
                    asset.get('model')
                } ({
                    asset.get('category')
                })",
                'value': asset
            } 
            for asset in asset_list if asset.get('category') == selected_term
            ],
            default=None
        ).execute()
        return choose
    def menu_select_action(self):
        choose = inquirer.select(
            message="Deseja gerar outro termo?: ",
            choices=[
            {
                'name': 'Gerar outro termo',
                'value': 'Generate'
            },
            {
                'name': 'Encerrar programa',
                'value': 'Exit'
            } 
            ],
            default=None
        ).execute()
        return choose