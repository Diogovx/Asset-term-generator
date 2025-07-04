from typing import Any

from InquirerPy import inquirer

from assets_term_generator.models import AppConfig, Asset


class Menu:
    def __init__(self, config: AppConfig):
        self.templates: dict[str, Any] = config.document.templates

    def input_employee_number(self) -> str:
        employee_number = inquirer.text(message="Digite a matricula:").execute()  # type: ignore[attr-defined]
        return employee_number

    def select_term(self) -> str:
        template_names = list(self.templates.keys())

        choose = inquirer.select(  # type: ignore[attr-defined]
            message="Você deseja gerar qual termo?\nEscolha um deles: ",
            choices=template_names,
            default=None,
        ).execute()
        return choose

    def select_asset(self, asset_list: list[Asset]) -> Asset:
        choose = inquirer.select(  # type: ignore[attr-defined]
            message="Foi encontrados mais de um ativo do usuário!\nEscolha um deles: ",
            choices=[
                {
                    "name": f"{asset.asset_tag} - {asset.model.name} ({asset.category.name})",
                    "value": asset,
                }
                for asset in asset_list
            ],
            default=None,
        ).execute()
        return choose

    def select_action(self) -> str:
        choose = inquirer.select(  # type: ignore[attr-defined]
            message="Deseja gerar outro termo?: ",
            choices=[
                {"name": "Gerar outro termo", "value": "Generate"},
                {"name": "Encerrar programa", "value": "Exit"},
            ],
            default=None,
        ).execute()
        return choose
