import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_base_path() -> Path:
    """Encontra a raiz do projeto procurando recursivamente pelo pyproject.toml."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    current_path = Path(__file__).resolve().parent

    while not (current_path / "pyproject.toml").exists():
        if current_path == current_path.parent:
            raise FileNotFoundError(
                "Não foi possível encontrar a raiz do projeto (marcador 'pyproject.toml')."
            )
        current_path = current_path.parent

    return current_path


# Path configuration
BASE_DIR = get_base_path()
CONFIG_DIR = BASE_DIR / "config"
CONFIG_FILE_PATH = CONFIG_DIR / "config.yml"
TEMPLATE_DIR = BASE_DIR / "docx-template"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
ENV_PATH = CONFIG_DIR / ".env"
ASSETS_PATH = BASE_DIR / "assets"


for directory in [TEMPLATE_DIR, OUTPUT_DIR, LOGS_DIR, CONFIG_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    logger.info(f"Arquivo .env não encontrado em {ENV_PATH}")

API_KEY = os.getenv("API_KEY")
API_HARDWARE_URL = os.getenv("API_HARDWARE_URL")
API_ACESSORIES_URL = os.getenv("API_ACESSORIES_URL")
API_COMPONENTS_URL = os.getenv("API_COMPONENTS_URL")
API_USERS_URL = os.getenv("API_USERS_URL")

ESSENTIAL_VARS = [
    API_KEY,
    API_HARDWARE_URL,
    API_ACESSORIES_URL,
    API_COMPONENTS_URL,
    API_USERS_URL,
]

if not all(ESSENTIAL_VARS):
    raise ValueError(
        "Uma ou mais variáveis de ambiente essenciais (API_KEY, URLs da API)"
        " não foram definidas no arquivo .env"
    )


if not API_KEY:
    logger.error("API_KEY não foi definida no .env")
