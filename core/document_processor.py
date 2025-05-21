import logging
from pathlib import Path
from typing import Any, Optional

from docx import Document

import api.snipeit_client as snipeit_client
from core.config_manager import LAPTOP_TEMPLATE_PATH, OUTPUT_DIR, SMARTPHONE_TEMPLATE_PATH
from models import Accessory, Asset, AssetList

logger = logging.getLogger(__name__)

MARKERS = {
    'NAME': '[NAME]',
    'EMPLOYEE_NUMBER': '[EMPLOYEE_NUMBER]',
    'HAS_LAPTOP': '[HASLAPTOP]',
    'LAPTOP_MODEL': '[LAPTOPMODEL]',
    'HAS_SMARTPHONE': '[HASSMARTPHONE]',
    'SMARTPHONE_MODEL': '[SMARTPHONEMODEL]',
    'HAS_MONITOR': "[HASMONITOR]",
    'MONITOR_MODEL': "[MONITORMODEL]",
    'HAS_CHARGER': "[HASCHARGER]",
    'CHARGER_MODEL': "[CHARGERMODEL]",
    'HAS_KEYBOARD': "[HASKEYBOARD]",
    'KEYBOARD_MODEL': "[KEYBOARDMODEL]",
    'HAS_MOUSE': "[HASMOUSE]",
    'MOUSE_MODEL': "[MOUSEMODEL]",
    'HAS_HEADSET': "[HASHEADSET]",
    'HEADSET_MODEL': "[HEADSETMODEL]",
    'HAS_SIMCARD': '[HASSIMCARD]',
    'SIMCARD_MODEL': '[SIMCARDMODEL]'
}

class DocumentProcessor:
    def __init__(self):
        self.document = None
    
    def load_template(self, selected_template) -> None:
        """ Load document template
        
        Raises:
            FileNotFoundErro: If model file not found
            Exception: For other error during loading
        """
        
        try:
            if selected_template == 'Laptops':
                if not LAPTOP_TEMPLATE_PATH.exists():
                    raise FileNotFoundError(f"Template not found at: {LAPTOP_TEMPLATE_PATH}")
                self.document = Document(str(LAPTOP_TEMPLATE_PATH))
                logger.info("Template carregado com sucesso")
            else:
                if not SMARTPHONE_TEMPLATE_PATH.exists():
                    raise FileNotFoundError(f"Template not found at: {SMARTPHONE_TEMPLATE_PATH}")
                self.document = Document(str(SMARTPHONE_TEMPLATE_PATH))
                logger.info("Template carregado com sucesso")
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            raise
    def _replace_in_paragraph(self, paragraph, key: str, value: str) -> None:
        """ Replace markers while maintaining formatting
        
        Args:
            paragraph: Document paragraph
            marker: Marker to be replaced (ex: [NAME])
            value: Replacement value
        """
        if key in paragraph.text:
            text = paragraph.text.replace(key, value)
            for run in paragraph.runs:
                run.text = ""
            paragraph.runs[0].text = text 
            
    def _check_assets(self, assetList, accessories_list) -> dict[str, bool]:
        assets_present = {
            'has_laptop': False,
            'has_smartphone': False,
            'has_monitor': False,
            'has_mouse': False,
            'has_keyboard': False,
            'has_charger': False,
            'has_headset': False,
            'has_simcard': False
        }
        for asset in assetList.get('assets'):
            if asset.get('category') == 'Laptops':
                assets_present['has_laptop'] = True
            if asset.get('category') == 'Smartphones':
                assets_present['has_smartphone'] = True

        for accessory in accessories_list:
            if accessory.get('category').get('name') == 'Charger':
                assets_present['has_charger'] = True
            if accessory.get('category').get('name') == 'Mouses':
                assets_present['has_mouse'] = True
            if accessory.get('category').get('name') == 'Keyboards':
                assets_present['has_keyboard'] = True
            if accessory.get('category').get('name') == 'Monitors':
                assets_present['has_monitor'] = True
            if accessory.get('category').get('name') == 'Headsets':
                assets_present['has_headset'] = True
            if accessory.get('category').get('name') == 'SIM Card':
                assets_present['has_simcard'] = True
        return assets_present
    
    def _process_asset_info(
        self, 
        assets_present: dict[str, bool], 
        asset_list: AssetList, 
        selected_asset: Asset, 
        accessories: list[Accessory]
    ) -> None:
        """Processes asset information and makes substitutions in the document.

        Args:
            assets_present (Dict[str, bool])
            asset_list (AssetList)
            selected_asset (Asset)
            accessories (List[Accessory])
        """
        ACCESSORY_CATEGORIES = [
            (
                'has_monitor', 
                'Monitors', 
                MARKERS['HAS_MONITOR'], 
                MARKERS['MONITOR_MODEL']
            ),
            (
                'has_mouse',
                'Mouses',
                MARKERS['HAS_MOUSE'],
                MARKERS['MOUSE_MODEL']
            ),
            (
                'has_keyboard', 
                'Keyboards', 
                MARKERS['HAS_KEYBOARD'], 
                MARKERS['KEYBOARD_MODEL']
            ),
            (
                'has_charger', 
                'Charger', 
                MARKERS['HAS_CHARGER'], 
                MARKERS['CHARGER_MODEL']
            ),
            (
                'has_headset', 
                'Headsets', 
                MARKERS['HAS_HEADSET'], 
                MARKERS['HEADSET_MODEL']
            ),
            (
                'has_simcard', 
                'SIM CARD', 
                MARKERS['HAS_SIMCARD'], 
                MARKERS['SIMCARD_MODEL']
            ),
        ]
        for paragraph in self.document.paragraphs:
            self._replace_in_paragraph(
                paragraph, 
                MARKERS['NAME'], 
                asset_list.get('user_name', '')
            )
            self._replace_in_paragraph(
                paragraph, 
                MARKERS['EMPLOYEE_NUMBER'], 
                asset_list.get('employee_number', '')
            )
            
            self._process_assets_type(paragraph, 
                                    assets_present.get('has_laptop'),
                                    MARKERS['HAS_LAPTOP'], 
                                    MARKERS['LAPTOP_MODEL'], 
                                    selected_asset if assets_present.get('has_laptop') else None
                                )
            self._process_assets_type(paragraph, 
                                    assets_present.get('has_smartphone'),
                                    MARKERS['HAS_SMARTPHONE'], 
                                    MARKERS['SMARTPHONE_MODEL'], 
                                    selected_asset if assets_present.get('has_smartphone') else None
                                )
            
            
            for key, name, presence_marker, description_marker in ACCESSORY_CATEGORIES:
                item = next(
                    (
                        accessory for accessory in accessories 
                        if accessory.get('category', {}).get('name') == name
                    ),
                    None
                )
                self._process_assets_type(
                    paragraph,
                    assets_present.get(key),
                    presence_marker,
                    description_marker,
                    item
                )
            

    def _process_assets_type(
        self, 
        paragraph, 
        has_asset: bool, 
        presence_marker: str, 
        description_marker: str, 
        item: Optional[Asset] = None
    ) -> None:
        """ Process a specific type of asset or accessory

        Args:
            paragraph:  Document paragraph
            has_asset (bool): If the item is present
            marker_check (str): Attendance marker
            marker_model (str): Template marker
            item (Optional[Asset]): Object containing item information
        """
        if not presence_marker or not description_marker:
            return
        
        self._replace_in_paragraph(
            paragraph,
            presence_marker,
            "X" if has_asset else " "
        )
        
        model_text = ""
        if has_asset and item:
            if isinstance(item, Asset) or hasattr(item, 'get'):
                model = item.get('model', item.get('name', ''))
                tag = item.get('asset_tag', '')
                serial = item.get('serial', '')
                if model and tag:
                    model_text = f"{model} - {tag} - {serial}"
                elif model:
                    model_text = model
                elif tag:
                    model_text = tag

        self._replace_in_paragraph(
            paragraph, 
            description_marker, 
            model_text
        )
        
    
    def process_assets(
        self,
        asset_list: dict[str, Any],
        selected_asset: Asset
    ) -> None:
        """Process asset list and update document

        Args:
            asset_list (Dict[str, Any]): User asset list
            selectedAsset (Asset): Asset selected for highlighting
        """
        try:
            if not self.document:
                raise ValueError("Documento não carregado. Chame load_template() primeiro.")
        
            accessories = snipeit_client.accessories_api_call(asset_list.get('user_id', ''))
            
            asset_linked_accessories = []
            if not accessories:
                accessories = snipeit_client.accessories_api_call(
                    selected_asset.get('asset_id'),
                    False
                )
                for accessory in accessories:
                    accessory_history = snipeit_client.specific_api_call(accessory.get('id', ''))
                    for checkout in accessory_history:
                        if checkout.get(
                            'assigned_to', {}
                        ).get(
                            'id', ''
                        ) == selected_asset.get(
                            'asset_id', ''
                        ):
                            asset_linked_accessories.append(accessory)
                accessories = asset_linked_accessories
                
            filtered_assets = self._check_assets(asset_list, accessories)
            
            self._process_asset_info(filtered_assets, asset_list, selected_asset, accessories)
            logger.info("Ativo processado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao processar o ativo: {e}")
            raise
    def save(self, username: str, asset_tag: str, type_of_term: str) -> Path:
        """Saves the processed document.

        Args:
            username (str): Username file name
            asset_tag (str): Asset tag to file name
            type_of_term (str): Term type for file name

        Returns:
            Path: File path
        """
        try:
            if not self.document:
                raise ValueError("Documento não carregado.")
            
            identifier = asset_tag.split('-')
            if len(identifier) < 2:
                raise ValueError(f"Formato de tag inválido: {asset_tag}")
            filename = (
                f"{identifier[1]} - Termo {type_of_term} - {username}.docx"
            )

            output_path = Path(OUTPUT_DIR) / filename
            self.document.save(output_path)
            logger.info(f"Termo de responsabilidade do usuário {username} criado!")
            return output_path
        except Exception as e:
            logger.error(f"Erro salvando o documento: {e}")
            raise        