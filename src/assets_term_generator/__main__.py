import logging

from requests.exceptions import RequestException

import assets_term_generator.api.snipeit_client as snipeit_client

from .core.config_handler import load_config
from .core.document_processor import DocumentProcessor
from .ui.cli_main import Menu
from .util import AssetNotFoundError, UserNotFoundError, configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    app_config = load_config()
    document_processor = DocumentProcessor(config=app_config)
    menu = Menu(config=app_config)

    while True:
        try:
            employee_number = menu.input_employee_number()
            if not employee_number:
                raise ValueError("Matrícula não pode ser vazia")
            user, assets = snipeit_client.get_user_and_assets(employee_number)

            selected_term = menu.select_term()
            document_processor.load_template(selected_term)

            filtered_assets = [
                asset
                for asset in assets
                if asset.category.name and asset.category.name.lower() == selected_term.lower()
            ]

            if not filtered_assets:
                raise ValueError(f"Usuário não possui ativo do tipo '{selected_term}'.")

            if len(filtered_assets) > 1:
                selected_asset = menu.select_asset(filtered_assets)
            else:
                selected_asset = filtered_assets[0]

            logger.info(f"Ativo selecionado: {selected_asset.model.name}")

            document_processor.process_document(user, selected_asset)

            file_path = document_processor.save(user.name, selected_asset.asset_tag, selected_term)
            document_processor.open_file(file_path)
            logger.info("Termo gerado com sucesso!")
        except (UserNotFoundError, AssetNotFoundError, ValueError) as e:
            logger.warning(e)
        except RequestException as e:
            logger.error(f"Erro de comunicação com a API do Snipe-IT: {e}")
        except Exception as e:
            logger.critical(f"Ocorreu um erro inesperado: {e}")

        input("\nPressione Enter para continuar...")

        selected_action = menu.select_action()
        if selected_action == "Exit":
            break


if __name__ == "__main__":
    main()
