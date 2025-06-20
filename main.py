import logging
import os

from InquirerPy import inquirer

import api.snipeit_client as snipeit_client
from core.document_processor import DocumentProcessor
from ui.cli_main import Menu
from util import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def main():
    document_processor = DocumentProcessor()
    menu = Menu()
    while True:
        try:
            assigned_to = inquirer.text(message="Digite a matricula:").execute()
            if not assigned_to:
                raise Exception("Matrícula não pode ser vazia")
        
            asset_list = snipeit_client.hardware_api_call(assigned_to)
            if not asset_list or not isinstance(asset_list, dict):
                raise Exception("Resposta inválida da API")
            assets = asset_list.get('assets', '')
            if not assets:
                raise Exception("Nenhum ativo encontrado para esta matricula")
            selected_term = menu.menu_select_term()
            document_processor.load_template(selected_term)
            filtered_assets = [asset for asset in assets
                if asset.get('category', '') == selected_term.capitalize()
            ]

            if not filtered_assets:
                raise ValueError(f"Nenhum ativo do tipo {selected_term} encontrado")
        
            if snipeit_client.has_multiple_assets(filtered_assets):
                selected_asset = menu.menu_select_asset(filtered_assets, selected_term)
            else:
                selected_asset = filtered_assets[0]

            logger.info(f"Ativo selecionado: {selected_asset.get('model', '')}")
            document_processor.process_assets(
                asset_list, selected_asset
            )
            file_path = document_processor.save(
                asset_list.get('user_name'), 
                selected_asset.get('asset_tag'), 
                selected_term
            )
            document_processor.open_file(file_path)
            
        except ValueError as ve:
            logger.error(f"Erro de seleção: {ve}")
        except Exception as e:
            logger.error(f"Erro ao processar termo: {e}")
        os.system("PAUSE")
        selected_action = menu.menu_select_action()
        if selected_action == 'Exit':
            break
        
if __name__ == "__main__":
    main()