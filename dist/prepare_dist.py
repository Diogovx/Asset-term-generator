import logging
import shutil
from pathlib import Path

"""from util import configure_logging

configure_logging()
logger = logging.getLogger(__name__)"""


def prepare_distribution():
    # Paths
    dist_dir = Path("dist/Gerador_de_Termos")
    final_dir = Path("Gerador_Termos_Final")

    (final_dir / "Gerador_Termos_Final").mkdir(parents=True, exist_ok=True)
    (final_dir / "docx-template").mkdir(parents=True, exist_ok=True)
    (final_dir / "output").mkdir(exist_ok=True)
    (final_dir / "config").mkdir(exist_ok=True)

    # Copy files
    shutil.copy("dist/Gerador_de_Termos.exe", final_dir)
    shutil.copy("README.md", final_dir)
    shutil.copy(
        "docx-template/TERMO DE RESPONSABILIDADES NOTEBOOKS.docx",
        final_dir / "docx-template",
    )
    shutil.copy(
        "docx-template/TERMO DE RESPONSABILIDADES CELULARES.docx",
        final_dir / "docx-template",
    )
    shutil.copy(
        "config/.env",
        final_dir / "config" / "docx-template",
    )
    shutil.copy(
        "config/config.yml",
        final_dir / "config" / "config.yml",
    )
    shutil.copy(
        "config/.env",
        final_dir / "config",
    )
    print(f"Distribution prepared in {final_dir}")


prepare_distribution()
