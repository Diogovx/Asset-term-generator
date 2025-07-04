from pydantic import BaseModel


class UIConfig(BaseModel):
    theme: str
    logo_path: str


class PlaceholderSource(BaseModel):
    type: str
    path: str | None = None
    value: str | None = None
    format: str | None = None


class Placeholder(BaseModel):
    name: str
    type: str
    category: str
    description: str
    default: bool
    required: bool
    identifier: bool
    source: PlaceholderSource
    generates_presence_marker: bool = False
    presence_marker_value: str | None = None


class TemplateConfig(BaseModel):
    file_name: str
    placeholders: list[Placeholder]


class DocumentConfig(BaseModel):
    template_path: str
    templates: dict[str, TemplateConfig]
    default_placeholders: list[Placeholder]


class AppConfig(BaseModel):
    ui: UIConfig
    document: DocumentConfig
