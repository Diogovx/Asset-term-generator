import logging
import webbrowser
from pathlib import Path

from docxtpl import DocxTemplate
from rich.console import Console

from assets_term_generator.models import AppConfig, Asset, TemplateConfig, User

from .config_manager import OUTPUT_DIR, TEMPLATE_DIR

logger = logging.getLogger(__name__)
console = Console()


class DocumentProcessor:
    def __init__(self, config: AppConfig) -> None:
        self.config: AppConfig = config
        self.document: DocxTemplate | None = None
        self.active_template_config: TemplateConfig

    def load_template(self, selected_template: str) -> None:
        """Load document template dynamically based on user selection.

        Args:
            selected_template (str): The name of the template to load.

        Raises:
            ValueError: If model not found in config file
            FileNotFoundErro: If model file not found
        """

        try:
            self.active_template_config = self.config.document.templates[selected_template]
            template_path = TEMPLATE_DIR / self.active_template_config.file_name
            self.document = DocxTemplate(template_path)
            logger.info(f"Template '{template_path.name}' carregado com sucesso.")
        except KeyError as e:
            raise KeyError(f"Template '{selected_template}' não encontrado na configuração.") from e
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Arquivo de template não encontrado em: {template_path}"
            ) from e

    def _prepare_context(self, user: User, selected_asset: Asset) -> dict:
        context = {
            "user": user,
            "asset": selected_asset,
            "accessories": selected_asset.accessories,
            "components": selected_asset.components,
            "display": self.active_template_config.display_names,
        }

        return context

    def process_document(self, user: User, selected_asset: Asset) -> None:
        """Process asset list and update document

        Args:
            asset_list (Dict[str, Any]): User asset list
            selectedAsset (Asset): Asset selected for highlighting
        """

        if not self.document:
            raise RuntimeError("Documento não carregado. Chame load_template() primeiro.")

        context = self._prepare_context(user, selected_asset)

        self.document.render(context)

        logger.info("Aplicando substituições no documento...")

    def save(self, username: str, asset_tag: str, type_of_term: str) -> Path:
        """Saves the processed document.

        Args:
            username (str): Username file name
            asset_tag (str): Asset tag to file name
            type_of_term (str): Term type for file name

        Returns:
            Path: File path
        """
        try:
            if not self.document:
                raise ValueError("Documento não carregado.")

            safe_username = "".join(c for c in username if c.isalnum() or c in " ._-")
            filename = f"{asset_tag} - Termo {type_of_term} - {safe_username}.docx"

            output_path = Path(OUTPUT_DIR) / filename
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            self.document.save(str(output_path))

            logger.info(f"Termo de responsabilidade do usuário {username} criado!")

            return output_path
        except ValueError as e:
            console.print("[bold red]SAVE ERROR[/bold red]: Erro salvando o documento.")
            logger.error(e)
            raise

    def open_file(self, file_path: Path) -> None:
        try:
            webbrowser.open(file_path.as_uri())
        except Exception as e:
            console.print("[bold red]OPENING ERROR[/bold red]: Erro ao abrir o arquivo ")
            logger.error(e)
