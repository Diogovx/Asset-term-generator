import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

logger = logging.getLogger(__name__)
console = Console()


def get_base_path() -> Path:
    """Finds the project root by recursively searching for pyproject.toml."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    try:
        current_path = Path(__file__).resolve().parent

        while not (current_path / "pyproject.toml").exists():
            if current_path == current_path.parent:
                raise FileNotFoundError("")
            current_path = current_path.parent
        return current_path  # noqa: TRY300

    except FileNotFoundError as e:
        console.print(
            "[bold red]FILE ERROR:"
            "Não foi possível encontrar a raiz do projeto (marcador 'pyproject.toml')."
        )
        console.print(f"[bold yellow]WARNING[/bold yellow]: Detalhes técnicos: {e}")
        logger.exception("Could not find project root")
        raise


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
try:
    if not all(ESSENTIAL_VARS):
        raise ValueError  # noqa: TRY301

except ValueError as e:
    console.print(
        "[bold red]ENV ERROR[/bold red]:"
        "Uma ou mais variáveis de ambiente essenciais (API_KEY, URLs da API)"
        " não foram definidas no arquivo .env"
    )
    console.print(f"[bold yellow]WARNING[/bold yellow]: Detalhes técnicos: {e}")
    logger.exception(
        "One or more essential environment variables (API_KEY, API URLs)"
        " were not defined in the .env file"
    )
