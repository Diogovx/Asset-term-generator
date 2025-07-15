import csv
import logging
from datetime import datetime
from getpass import getuser
from pathlib import Path
from typing import Any

from rich.console import Console

from assets_term_generator.core.config_manager import LOGS_DIR
from assets_term_generator.models import Asset, User

logger = logging.getLogger(__name__)
console = Console()

HISTORY_FILE = LOGS_DIR / "generation_history.csv"
FIELD_NAMES = [
    "timestamp",
    "user_generator",
    "employee_number",
    "employee_name",
    "asset_tag",
    "asset_model",
    "user_template",
    "generated_term_path",
]


def log_generation_history(user: User, asset: Asset, template_name: str, output_path: Path) -> None:
    try:
        LOGS_DIR.mkdir(exist_ok=True)
        file_exists = HISTORY_FILE.exists()

        with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)

            if not file_exists:
                writer.writeheader()

            history_entry: dict[str, Any] = {
                "timestamp": datetime.now().isoformat(),
                "user_generator": getuser(),
                "employee_number": user.employee_num,
                "employee_name": user.name,
                "asset_tag": asset.asset_tag,
                "asset_model": asset.model.name,
                "user_template": template_name,
                "generated_term_path": output_path,
            }
            writer.writerow(history_entry)

            logger.info(f"Registro de histórico adicionado em '{HISTORY_FILE}'")
    except Exception as e:
        console.print("[bold red]HISTORY ERROR: Falha ao escrever no arquivo de histórico")
        logger.error(e)
