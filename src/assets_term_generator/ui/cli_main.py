import logging
from typing import Any

from InquirerPy import inquirer

from assets_term_generator.models import AppConfig, Asset
from assets_term_generator.util import NoCompatibleAssetsError

logger = logging.getLogger(__name__)


class Menu:
    def __init__(self, config: AppConfig):
        self.templates: dict[str, Any] = config.document.templates

    def input_employee_number(self) -> str:
        employee_number = inquirer.text(message="Digite a matricula:").execute()  # type: ignore[attr-defined]
        return employee_number

    def select_document_type(self) -> str:
        choices = [
            {"name": info.description, "value": name} for name, info in self.templates.items()
        ]
        select_type = inquirer.select(  # type: ignore[attr-defined]
            message="Qual tipo de documento você deseja gerar?",
            choices=choices,
        ).execute()
        return select_type

    def select_asset_category(self, available_categories: list[str]) -> str:
        """Exibe um menu para o usuário escolher uma categoria de ativo.

        Args:
            available_categories (list[str]): A lista de categorias que o usuário possui.

        Returns:
            str: A categoria selecionada pelo usuário.
        """
        if not available_categories:
            raise NoCompatibleAssetsError(available_categories)

        if len(available_categories) == 1:
            selected_category = available_categories[0]
            logger.info(
                f"Categoria '{selected_category}'selecionada automaticamente (única opção)."
            )
            return selected_category

        selected_category = inquirer.select(  # type: ignore[attr-defined]
            message="O usuário possui ativos em várias categorias."
            "Para qual delas deseja gerar o termo?",
            choices=available_categories,
        ).execute()

        return selected_category

    def select_category(self, avalible_categories: list[str]) -> str:
        choose = inquirer.select(  # type: ignore[attr-defined]
            message="Você deseja gerar qual termo?\nEscolha um deles: ",
            choices=avalible_categories,
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

    def confirm_action(self) -> str:
        choose = inquirer.confirm(  # type: ignore[attr-defined]
            message="Tudo certo para gerar o documento?", default=True
        ).execute()
        return choose
