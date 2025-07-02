import logging
import os
import platform
import subprocess
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.text.paragraph import Paragraph

from core.config_manager import OUTPUT_DIR, TEMPLATE_DIR
from core.models import AppConfig, Asset, TemplateConfig, User

logger = logging.getLogger(__name__)


def docx_replace(paragraph: Paragraph, old_text: str, new_text: str):
    for run in paragraph.runs:
        if old_text in run.text:
            run.text = run.text.replace(old_text, new_text)


class DocumentProcessor:
    def __init__(self, config: AppConfig) -> None:
        self.config: AppConfig = config
        self.document: DocumentObject | None = None
        self.active_template_config: TemplateConfig | None = None

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
            self.document = Document(str(template_path))
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
        }
        return context

    def _resolve_placeholders(self, context: dict) -> dict:
        """
        Usa o contexto para resolver o valor final de cada placeholder da configuração.
        Retorna um dicionário de {'[PLACEHOLDER]': 'valor_final'}.
        """
        if not self.active_template_config:
            raise RuntimeError("Template não foi carregado. Chame load_template() primeiro.")

        all_placeholders = (
            self.active_template_config.placeholders + self.config.document.default_placeholders
        )

        replacements = {}
        user = context["user"]
        asset = context["asset"]

        for ph in all_placeholders:
            source = ph.source
            value = ""
            if source.type == "text" and source.path:
                value = getattr(user, source.path, "")
            elif source.type == "asset" and source.format:
                value = source.format.format(
                    model=asset.model.name, asset_tag=asset.asset_tag, serial=asset.serial or ""
                )
            elif source.type in ["accessories", "components"]:
                item_list = context.get(source.type, [])

                def get_category_name(item):
                    if not item.category:
                        return ""
                    if isinstance(item.category, str):
                        return item.category
                    return item.category.name

                found_item = next(
                    (item for item in item_list if get_category_name(item) == ph.category), None
                )
                print(item_list)

                if found_item:
                    if source.format:
                        format_context = {
                            "name": found_item.name or "",
                            "numero_do_celular": asset.get_custom_field("NUMERO") or "",
                        }
                        value = source.format.format(**format_context)
                    elif source.path:
                        value = getattr(found_item, source.path, "") or ""

            replacements[ph.name] = str(value)

            if ph.generates_presence_marker:
                base_name = ph.name.strip("[]").replace("MODEL", "")
                presence_marker_name = f"[HAS{base_name}]"

                if value:
                    replacements[presence_marker_name] = ph.presence_marker_value or "X"
                else:
                    replacements[presence_marker_name] = ""
        return replacements

    def _replace_in_paragraph(self, paragraph: Paragraph, key: str, value: str) -> None:
        """Replace markers while maintaining formatting

        Args:
            paragraph: Document paragraph
            marker: Marker to be replaced (ex: [NAME])
            value: Replacement value
        """
        if key in paragraph.text:
            text = paragraph.text.replace(key, value)
            for run in paragraph.runs:
                run.text = ""
            paragraph.runs[0].text = text

    def process_document(self, user: User, selected_asset: Asset) -> None:
        """Process asset list and update document

        Args:
            asset_list (Dict[str, Any]): User asset list
            selectedAsset (Asset): Asset selected for highlighting
        """

        if not self.document:
            raise RuntimeError("Documento não carregado. Chame load_template() primeiro.")

        context = self._prepare_context(user, selected_asset)

        replacements = self._resolve_placeholders(context)

        logger.info("Aplicando substituições no documento...")
        for paragraph in self.document.paragraphs:
            for placeholder, value in replacements.items():
                docx_replace(paragraph, placeholder, value)

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
            self.document.save(str(output_path))
            logger.info(f"Termo de responsabilidade do usuário {username} criado!")
            return output_path
        except Exception as e:
            logger.error(f"Erro salvando o documento: {e}")
            raise

    def open_file(self, file_path: Path) -> None:
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        except Exception as e:
            logger.error(f"Erro ao abrir o arquivo {e}")
