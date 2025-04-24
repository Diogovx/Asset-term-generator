from pathlib import Path
import sys
import os

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

# Path configuration
BASE_DIR = get_base_path()
TEMPLATE_PATH = BASE_DIR / "docx-template" / "TERMO DE RESPONSABILIDADES NOTEBOOKS.docx"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)