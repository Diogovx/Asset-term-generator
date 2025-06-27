from typing import Literal

from pydantic import BaseModel, Field


class UIConfig(BaseModel):
    theme: str
    logo_path: str

class AssetSource(BaseModel):
    type: Literal["asset"]
    format: str

class AccessorySource(BaseModel):
    type: Literal["accessories", "components"]
    path: str

class LiteralSource(BaseModel):
    type: Literal["literal"]
    value: str

class TextSource(BaseModel):
    type: Literal["text"]
    path: str

class Placeholder(BaseModel):
    name: str
    type: str
    category: str
    description: str
    default: bool
    required: bool
    identifier: bool
    source: AssetSource | AccessorySource | LiteralSource | TextSource = Field(discriminator="type")

class TemplateConfig(BaseModel):
    template_name: str
    Placeholders: dict[str, Placeholder]

class DocumentConfig(BaseModel):
    template_path: str
    templates: dict[str, TemplateConfig]
    default_placeholders: list[Placeholder]

class AppConfig(BaseModel):
    ui: UIConfig
    document: DocumentConfig