import sys
from pathlib import Path
import logging
# Logging configuration
def configure_logging():
    
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).parent.parent
    
    # Create log dir if not exists
    log_dir = base_dir / 'logs'
    log_dir.mkdir(exist_ok=True, parents=True)
    
    log_file = log_dir / 'termo_responsabilidade.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(str(log_file)),
            logging.StreamHandler()
        ]
)