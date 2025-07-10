import logging

from requests.exceptions import RequestException

from assets_term_generator.api import snipeit_client
from assets_term_generator.core.config_handler import load_config
from assets_term_generator.core.document_processor import DocumentProcessor
from assets_term_generator.ui.cli_main import Menu
from assets_term_generator.util.exceptions import AssetNotFoundError, UserNotFoundError
from assets_term_generator.util.history_logging import log_generation_history
from assets_term_generator.util.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    app_config = load_config()
    document_processor = DocumentProcessor(config=app_config)
    menu = Menu(config=app_config)

    while True:
        try:
            document_key = menu.select_document_type()

            employee_number = menu.input_employee_number()
            if not employee_number:
                raise ValueError("Matrícula não pode ser vazia")
            
            user, assets = snipeit_client.get_user_and_assets(employee_number)
            if not assets:
                raise AssetNotFoundError(f"Nenhum ativo encontrado para o usuário '{user.name}'.")

            user_categories = sorted(list({
                asset.category.name for asset in assets if asset.category and asset.category.name
            }))

            selected_category = menu.select_asset_category(user_categories)
            logger.info(f"Categoria selecionada para o termo: '{selected_category}'")

            assets_in_category = [
                asset for asset in assets
                if asset.category and asset.category.name == selected_category
            ]

            if len(assets_in_category) > 1:
                selected_asset = menu.select_asset(assets_in_category)
            else:
                selected_asset = assets_in_category[0]
            
            logger.info(f"Ativo principal selecionado para o termo: {selected_asset.asset_tag}")

            document_processor.load_template(document_key)
            document_processor.process_document(user, selected_asset)
            file_path = document_processor.save(
                user.name,
                selected_asset.asset_tag,
                document_key
            )
            
            log_generation_history(user, selected_asset, document_key, file_path)
            document_processor.open_file(file_path)
            
            logger.info("Termo gerado com sucesso!")

        except (UserNotFoundError, AssetNotFoundError, ValueError) as e:
            logger.warning(e)
        except RequestException as e:
            logger.error(f"Erro de comunicação com a API do Snipe-IT: {e}")
        except Exception as e:
            logger.critical(f"Ocorreu um erro inesperado: {e}", exc_info=True)

        input("\nPressione Enter para continuar...")

        selected_action = menu.select_action()
        if selected_action == "Exit":
            break


if __name__ == "__main__":
    main()
