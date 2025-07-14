from pydantic import BaseModel


class UIConfig(BaseModel):
    theme: str
    logo_path: str


class CategoryDisplayNames(BaseModel):
    Charger: str | None = "Charger"
    Monitors: str | None = "Monitors"
    Mouses: str | None = "Mouses"
    Keyboards: str | None = "Keyboards"
    Headsets: str | None = "Headsets"
    ...

    class Config:
        extra = "allow"


class DisplayNames(BaseModel):
    categories: CategoryDisplayNames


class TemplateConfig(BaseModel):
    file_name: str
    display_names: DisplayNames
    description: str | None = None
    target_categories: list[str] | None = None


class DocumentConfig(BaseModel):
    template_path: str
    templates: dict[str, TemplateConfig]


class AppConfig(BaseModel):
    ui: UIConfig
    document: DocumentConfig
