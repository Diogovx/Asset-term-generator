import logging
import shutil
from pathlib import Path

from assets_term_generator.core.config_handler import load_config
from assets_term_generator.core.config_manager import BASE_DIR, CONFIG_DIR, TEMPLATE_DIR
from assets_term_generator.util import configure_logging

logger = logging.getLogger(__name__)


def prepare_distribution() -> None:
    app_config = load_config()
    # Paths
    final_dir = Path("Assets_term_generator")
    dist_exe_path = BASE_DIR / "dist" / "Assets_term_generator.exe"

    logger.info("Checking if required files exist...")
    if not dist_exe_path.exists():
        logger.critical(
            f"ERROR: Executable not found at '{dist_exe_path}'. Please run PyInstaller first."
        )
        return

    logger.info(f"Cleaning up the final directory: {final_dir}")
    if final_dir.exists():
        shutil.rmtree(final_dir)

    final_template_dir = final_dir / "docx-template"
    final_config_dir = final_dir / "config"
    final_template_dir.mkdir(parents=True, exist_ok=True)
    final_config_dir.mkdir(exist_ok=True)

    (final_dir / "output").mkdir(exist_ok=True)
    (final_dir / "logs").mkdir(exist_ok=True)

    # Copy files
    logger.info("Copiando arquivos...")
    shutil.copy(dist_exe_path, final_dir)
    shutil.copy(BASE_DIR / "README.md", final_dir)
    shutil.copy(BASE_DIR / "README.pt-br.md", final_dir)
    shutil.copy(BASE_DIR / "USER_MANUAL.md", final_dir)
    shutil.copy(BASE_DIR / "USER_MANUAL.pt-br.md", final_dir)
    shutil.copy(
        CONFIG_DIR / "config.yml",
        final_config_dir,
    )
    shutil.copy(
        CONFIG_DIR / ".env.example",
        final_config_dir,
    )

    logger.info("Copying document templates...")
    templates_config = app_config.document.templates
    for _, template_info in templates_config.items():
        file_name = template_info.file_name
        if file_name:
            source_path = TEMPLATE_DIR / file_name
            logger.info(f"Template '{file_name}' copiado.")
        else:
            logger.warning(
                f"Template '{file_name} defined in config.yml but not found in {source_path}"
            )

    logger.info(f"Distruibution prepared in {final_dir}")


if __name__ == "__main__":
    configure_logging()
    prepare_distribution()
