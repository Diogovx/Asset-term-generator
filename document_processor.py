from docx import Document
from typing import Dict, Any
import api_call
from pathlib import Path
import logging
from config import TEMPLATE_PATH, OUTPUT_DIR


logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self):
        self.document = None
    
    def load_template(self) -> None:
        """ Load document template """
        
        try:
            if not TEMPLATE_PATH.exists():
                raise FileNotFoundError(f"Template not found at: {TEMPLATE_PATH}")
            self.document = Document(str(TEMPLATE_PATH))
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            raise
    def replace_in_paragraph(self, paragraph, key: str, value: str) -> None:
        """ Replace markers while maintaining formatting """
        if key in paragraph.text:
            for run in paragraph.runs:
                if key in run.text:
                    run.text = run.text.replace(key, value)
    def process_assets(self, assetList: Dict[str, Any]):
        hasLaptop = False
        hasMonitor = False
        hasMouse = False
        hasKeyboard = False
        hasCharger = False
        hasHeadset = False
        
        user_id = assetList.get('user_id')
        accessoriesList = api_call.accessoriesApiCall(user_id)
        
        for asset in assetList.get('assets'):
            if asset.get('category') == 'Laptops':
                hasLaptop = True

        for accessory in accessoriesList:
            if accessory.get('category').get('name') == 'Charger':
                hasCharger = True
            if accessory.get('category').get('name') == 'Mouses':
                hasMouse = True
            if accessory.get('category').get('name') == 'Keyboards':
                hasKeyboard = True
            if accessory.get('category').get('name') == 'Monitors':
                hasMonitor = True
            if accessory.get('category').get('name') == 'Headsets':
                hasHeadset = True

        for paragraph in self.document.paragraphs:
            self.replace_in_paragraph(paragraph, "[NAME]", assetList.get('user_name', ''))
            self.replace_in_paragraph(paragraph, "[EMPLOYEE_NUMBER]", assetList.get('employee_number', ''))
    
            if hasLaptop:
                self.replace_in_paragraph(paragraph, "[HASLAPTOP]", "X")
                for asset in assetList.get('assets', []):
                    if asset.get('category') == 'Laptops':
                        self.replace_in_paragraph(paragraph, "[LAPTOPMODEL]", f"{asset.get('model', '')} - {asset.get('asset_tag')}")
            else:
                self.replace_in_paragraph(paragraph, "[HASLAPTOP]", " ")
                self.replace_in_paragraph(paragraph, "[LAPTOPMODEL]", "")
                
            if hasMonitor:
                self.replace_in_paragraph(paragraph, "[HASMONITOR]", "X")
                for accessory in accessoriesList:
                    if accessory.get('category').get('name') == 'Monitors':
                        self.replace_in_paragraph(paragraph, "[MONITORMODEL]", f"{accessory.get('name', '')} - {accessory.get('model_number', '')}")
            else:
                self.replace_in_paragraph(paragraph, "[HASMONITOR]", " ")
                self.replace_in_paragraph(paragraph, "[MONITORMODEL]", "")
            
            if hasCharger:
                self.replace_in_paragraph(paragraph, "[HASCHARGER]", "X")
                for accessory in accessoriesList:
                    if accessory.get('category').get('name') == 'Charger':
                        self.replace_in_paragraph(paragraph, "[CHARGERMODEL]", f"{accessory.get('name', ' ')}")
            else:
                self.replace_in_paragraph(paragraph, "[HASCHARGER]", " ")
                self.replace_in_paragraph(paragraph, "[CHARGERMODEL]", "")
            
            if hasKeyboard:
                self.replace_in_paragraph(paragraph, "[HASKEYBOARD]", "X")
                for accessory in accessoriesList:
                    if accessory.get('category').get('name') == 'Keyboards':
                        self.replace_in_paragraph(paragraph, "[KEYBOARDMODEL]", f"{accessory.get('name', '')} - {accessory.get('model_number', '')}")
            else:
                self.replace_in_paragraph(paragraph, "[HASKEYBOARD]", " ")
                self.replace_in_paragraph(paragraph, "[KEYBOARDMODEL]", "")
            
            if hasMouse:
                self.replace_in_paragraph(paragraph, "[HASMOUSE]", "X")
                for accessory in accessoriesList:
                    if accessory.get('category').get('name') == 'Mouses':
                        self.replace_in_paragraph(paragraph, "[MOUSEMODEL]", f"{accessory.get('name', '')} - {accessory.get('model_number', '')}")
            
            else:
                self.replace_in_paragraph(paragraph, "[HASMOUSE]", " ")
                self.replace_in_paragraph(paragraph, "[MOUSEMODEL]", "")
            
            if hasHeadset:
                self.replace_in_paragraph(paragraph, "[HASHEADSET]", "X")
                for accessory in accessoriesList:
                    if accessory.get('category').get('name') == 'Headsets':
                        self.replace_in_paragraph(paragraph, "[HEADSETMODEL]", f"{accessory.get('name', '')} - {accessory.get('model_number', '')}")
            else:
                self.replace_in_paragraph(paragraph, "[HASHEADSET]", " ")
                self.replace_in_paragraph(paragraph, "[HEADSETMODEL]", "")
        
    def save(self, username: str) -> Path:
        self.document.save(str(OUTPUT_DIR) + "/" + f"Termo - {username}.docx")
        pass