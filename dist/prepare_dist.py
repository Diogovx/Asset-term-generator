import logging
import shutil
from pathlib import Path

from util import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

def prepare_distribution():
    # Paths
    dist_dir = Path('dist/Gerador_de_Termos')
    final_dir = Path('Gerador_Termos_Final')
    
    (final_dir / 'docx-template').mkdir(parents=True, exist_ok=True)
    (final_dir / 'output').mkdir(exist_ok=True)
    
    # Copy files
    shutil.copy(dist_dir / 'Gerador_de_Termos.exe', final_dir)
    shutil.copy('Gerador_de_Termos/README.md', final_dir)
    shutil.copy(
        dist_dir / 'docx-template/TERMO DE RESPONSABILIDADES NOTEBOOKS.docx',
        final_dir / 'docx-template'
    )
    shutil.copy(
        dist_dir / 'docx-template/TERMO DE RESPONSABILIDADES CELULARES.docx',
        final_dir / 'docx-template'
    )
    logger.info(f"Distribution prepared in {final_dir}")

if(__name__ == "__main__"):
    prepare_distribution()