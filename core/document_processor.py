import logging
import os
import platform
import re
import subprocess
from pathlib import Path
from typing import Any, cast

from docx import Document
from docx.text.paragraph import Paragraph

import api.snipeit_client as snipeit_client
import core.template_loader as template_loader
from core.config_manager import OUTPUT_DIR

logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self) -> None:
        self.document: Document | None = None
        self.template_placeholders: list

    def load_template(self, selected_template: str) -> None:
        """Load document template dynamically based on user selection.

        Args:
            selected_template (str): The name of the template to load.

        Raises:
            ValueError: If model not found in config file
            FileNotFoundErro: If model file not found
        """

        try:
            config = template_loader.load_config_file()
            document_config = config.get("document", {})
            templates = document_config.get("templates", {})

            template_info = templates.get(selected_template)
            if not template_info:
                raise ValueError(f"Template {selected_template} not found in config")

            template_path = Path(
                document_config.get("template_path", "")
            ) / template_info.get("file_name", "")
            if not template_path.exists():
                raise FileNotFoundError(f"Template not found at: {template_path}")

            self.document = Document(str(template_path))
            self.template_placeholders = template_info.get("placeholders")

            logger.info(
                f"Template {template_info.get('file_name', '')} carregado em {template_path}"
            )

        except Exception as e:
            logger.error(f"Error loading template '{selected_template}': {e}")
            raise

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

    def _check_assets(
        self, asset_list: dict, accessories_list: list, components_list: list
    ) -> dict[str, bool]:
        """_summary_

        Args:
            asset_list: assets dictionary
            accessories_list: accessories dictionary

        Returns:
            dict[str, bool]: check presence of assets and accessories
        """
        assets_present = {}
        for asset in asset_list.get("assets", []):
            category = asset.get("category", "")
            if isinstance(category, dict):
                category = category.get("name", "")
            key = f"has_{category.lower()}"
            assets_present[key] = True

        for accessory in accessories_list:
            category = accessory.get("category", {})
            if category:
                key = f"has_{category.lower()}"
                assets_present[key] = True

        for component in components_list:
            category = component.get("category", {})
            if category:
                key = f"has_{category.lower()}"
                assets_present[key] = True

        return assets_present

    def _process_placeholder(
        self,
        paragraph: Paragraph,
        selected_asset: dict[str, Any],
        asset_list: dict[str, Any],
        assets_present: dict[str, bool],
    ) -> None:
        """Processes asset information and makes substitutions in the document.

        Args:

            assets_present (Dict[str, bool])
            asset_list (AssetList)
            selected_asset (Asset)
            accessories (List[Accessory])
            selected_template (str)

        """
        accessories = selected_asset.get("accessories", "")
        components = selected_asset.get("components", "")
        for item in self.template_placeholders:
            placeholder = item.get("name", "")
            item_category = item.get("category", "")
            if isinstance(item_category, dict):
                item_category = item_category.get("name", "")
            item_type = item.get("type", "")
            data_source = item.get("source", {})
            data_path = data_source.get("path", data_source.get("value", ""))

            if not placeholder or not data_path:
                logger.warning(f"Placeholder inválido ou incompleto: {item}")
                continue

            if item_type == "bool":
                key = f"has_{item_category.lower()}"
                value = data_path if assets_present.get(key, False) else ""

            elif data_source.get("type", "") == "accessories":
                category_to_find = item.get("category", "")
                accessory = next(
                    (
                        acc
                        for acc in accessories
                        if acc.get("category", "").lower() == category_to_find.lower()
                    ),
                    None,
                )
                if accessory:
                    value = accessory.get(data_path, "")
                else:
                    value = ""

            elif data_source.get("type", "") == "components":
                category_to_find = item.get("category", "")
                accessory = next(
                    (
                        comp
                        for comp in components
                        if comp.get("category", "").lower() == category_to_find.lower()
                    ),
                    None,
                )
                if accessory:
                    value = accessory.get(data_path, "")
                else:
                    value = ""

            else:
                model = selected_asset.get(data_path, "")
                tag = selected_asset.get("asset_tag", "")
                serial = selected_asset.get("serial", "")
                if model and tag:
                    value = f"{model} - {tag} - {serial}"
                elif model:
                    value = model
                elif tag:
                    value = tag

            self._replace_in_paragraph(paragraph, placeholder, value)

    def _process_default_placeholders(
        self, paragraph: Paragraph, asset_list: dict[str, Any]
    ) -> None:
        """Replaces the default placeholders as per the configuration file

        Args:
            paragraph (_type_): _description_
            asset_list (_type_): _description_
        """
        config = template_loader.load_config_file()
        default_placeholders = config.get("document", {}).get(
            "default_placeholders", {}
        )

        for entry in default_placeholders:
            placeholder = entry.get("name")
            data_path = entry.get("source", {}).get("path")

            if not placeholder or not data_path:
                logger.warning(f"Placeholder inválido ou incompleto: {entry}")
                continue

            value = asset_list.get(data_path, "")
            self._replace_in_paragraph(paragraph, placeholder, value)

    def process_assets(
        self, asset_list: dict[str, Any], selected_asset: dict[str, Any]
    ) -> None:
        """Process asset list and update document

        Args:
            asset_list (Dict[str, Any]): User asset list
            selectedAsset (Asset): Asset selected for highlighting
        """
        try:
            if not self.document:
                raise ValueError(
                    "Documento não carregado. Chame load_template() primeiro."
                )

            components: list[dict[str, Any]] = snipeit_client.components_api_call()
            asset_linked_components = []
            if components:
                for component in components:
                    components_history = snipeit_client.specific_component_api_call(
                        component.get("id", "")
                    )
                    for checkout in components_history:
                        name = checkout.get("name", "")
                        match = re.search(r"\(([^\)]+)\)", name)

                        # extracted_tag = match.group(1).strip().upper()
                        if match:
                            extracted_tag = match.group(1).strip().upper()
                            if extracted_tag == selected_asset.get("asset_tag"):
                                asset_linked_components.append(
                                    {
                                        "component_id": component.get("id", ""),
                                        "name": component.get("name"),
                                        "category": component.get("category", {}).get(
                                            "name", ""
                                        ),
                                    }
                                )
                components = asset_linked_components
            selected_asset["components"] = components

            accessories = snipeit_client.accessories_api_call(
                asset_list.get("user_id", "")
            )
            asset_linked_accessories = []
            if not accessories:
                accessories = snipeit_client.accessories_api_call(
                    cast(int, selected_asset.get("asset_id")), False
                )

                for accessory in accessories:
                    accessory_history = snipeit_client.specific_accessory_api_call(
                        accessory.get("id", "")
                    )
                    for checkout in accessory_history:
                        if checkout.get("assigned_to", {}).get(
                            "id", ""
                        ) == selected_asset.get("asset_id", ""):
                            asset_linked_accessories.append(
                                {
                                    "accessory_id": accessory.get("id", ""),
                                    "name": accessory.get("name"),
                                    "category": accessory.get("category", {}).get(
                                        "name", ""
                                    ),
                                }
                            )
                accessories = asset_linked_accessories
            selected_asset["accessories"] = accessories
            assets_present = self._check_assets(asset_list, accessories, components)
            for paragraph in self.document.paragraphs:
                self._process_default_placeholders(paragraph, asset_list)
                self._process_placeholder(
                    paragraph, selected_asset, asset_list, assets_present
                )

            logger.info("Ativo processado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao processar o ativo: {e}")
            raise

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

            identifier = asset_tag.split("-")
            if len(identifier) < 2:
                raise ValueError(f"Formato de tag inválido: {asset_tag}")
            filename = f"{identifier[1]} - Termo {type_of_term} - {username}.docx"

            output_path = Path(OUTPUT_DIR) / filename
            self.document.save(output_path)
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
