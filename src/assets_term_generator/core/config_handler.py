import logging

from pydantic import ValidationError
from yaml import safe_dump, safe_load

from assets_term_generator.models.config_models import AppConfig
from assets_term_generator.util import configure_logging

from .config_manager import CONFIG_FILE_PATH

configure_logging()
logger = logging.getLogger(__name__)


def load_config() -> AppConfig:
    try:
        with open(CONFIG_FILE_PATH, encoding="utf-8") as f:
            data = safe_load(f)

        return AppConfig(**data)
    except FileNotFoundError:
        logger.critical(
            f"ERRO FATAL: Arquivo de configuração não encontrado em '{CONFIG_FILE_PATH}'."
            "O programa não pode continuar."
        )
        raise
    except ValidationError as e:
        logger.critical(
            "ERRO FATAL: O arquivo 'config.yml' contém erros de estrutura ou tipos."
            f"Por favor, verifique.\nDetalhes: {e}"
        )
        raise
    except Exception as e:
        logger.critical(f"Ocorreu um erro inesperado ao carregar a configuração: {e}")
        raise


def save_config(config: AppConfig) -> None:
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        config_dict = config.model_dump(mode="json")
        safe_dump(config_dict, f, allow_unicode=True, sort_keys=False)
