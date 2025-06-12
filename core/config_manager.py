import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent


# Path configuration
BASE_DIR = get_base_path()
CONFIG_DIR = BASE_DIR / "config"
CONFIG_FILE_PATH = CONFIG_DIR / "config.yml"
TEMPLATE_DIR = BASE_DIR / "docx-template"
LAPTOP_TEMPLATE_PATH = TEMPLATE_DIR / "TERMO DE RESPONSABILIDADES NOTEBOOKS.docx"
SMARTPHONE_TEMPLATE_PATH = TEMPLATE_DIR / "TERMO DE RESPONSABILIDADES CELULARES.docx"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
ENV_PATH = CONFIG_DIR / ".env"
ASSETS_PATH = BASE_DIR / "assets"


for directory in [TEMPLATE_DIR ,OUTPUT_DIR, LOGS_DIR, CONFIG_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    logger.info(f"Arquivo .env não encontrado em {ENV_PATH}")

API_KEY = os.getenv("API_KEY")
API_HARDWARE_URL = os.getenv("API_HARDWARE_URL")
API_ACESSORIES_URL = os.getenv("API_ACESSORIES_URL")
API_USERS_URL = os.getenv("API_USERS_URL")

if not API_KEY:
    logger.error("API_KEY não foi definida no .env")