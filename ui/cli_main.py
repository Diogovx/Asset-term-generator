from typing import Any

from InquirerPy import inquirer

from core.template_loader import get_templates


class Menu:
    def menu_select_term(self) -> str:
        template_config = get_templates()

        choose = inquirer.select(
            message="Você deseja gerar qual termo?\nEscolha um deles: ",
            choices=[
                {
                    "name": template,
                    "value": template,
                }
                for template in template_config
            ],
            default=None,
        ).execute()
        return choose

    def menu_select_asset(self, asset_list: list) -> dict[str, Any]:
        choose = inquirer.select(
            message="Foi encontrados mais de um ativo do usuário!\nEscolha um deles: ",
            choices=[
                {
                    "name": f"{
                    asset.get('asset_tag')
                } - {
                    asset.get('model')
                } ({
                    asset.get('category')
                })",
                    "value": asset,
                }
                for asset in asset_list
            ],
            default=None,
        ).execute()
        return choose

    def menu_select_action(self) -> str:
        choose = inquirer.select(
            message="Deseja gerar outro termo?: ",
            choices=[
                {"name": "Gerar outro termo", "value": "Generate"},
                {"name": "Encerrar programa", "value": "Exit"},
            ],
            default=None,
        ).execute()
        return choose
