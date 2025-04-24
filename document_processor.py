from docx import Document
from typing import Dict, Any
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

        for asset in assetList.get('assets'):
            if asset.get('category') == 'Laptops':
                hasLaptop = True
            if asset.get('category') == 'Monitors':
                hasMonitor = True


        for paragraph in self.document.paragraphs:
            self.replace_in_paragraph(paragraph, "[NAME]", assetList.get('user_name', ''))
            self.replace_in_paragraph(paragraph, "[EMPLOYEE_NUMBER]", assetList.get('employee_number', ''))
    
            if hasLaptop:
                self.replace_in_paragraph(paragraph, "[ISLAPTOPS]", "X")
                for asset in assetList.get('assets', []):
                    if asset.get('category') == 'Laptops':
                        self.replace_in_paragraph(paragraph, "[LAPTOPMODEL]", asset.get('model', ''))
            else:
                self.replace_in_paragraph(paragraph, "[ISLAPTOPS]", " ")
                self.replace_in_paragraph(paragraph, "[LAPTOPMODEL]", "_____________________________")
    
            if hasMonitor:
                self.replace_in_paragraph(paragraph, "[ISMONITORS]", "X")
                for asset in assetList.get('assets', []):
                    if asset.get('category') == 'Monitors':
                        self.replace_in_paragraph(paragraph, "[MONITORMODEL]", asset.get('model', ''))
            else:
                self.replace_in_paragraph(paragraph, "[ISMONITORS]", " ")
                self.replace_in_paragraph(paragraph, "[MONITORMODEL]", "_____________________________")
        
    def save(self, username: str) -> Path:
        self.document.save(str(OUTPUT_DIR) + "/" + f"Termo - {username}.docx")
        pass