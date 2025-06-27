from typing import Any

from pydantic import BaseModel, Field


class AssetModel(BaseModel):
    id: int
    name: str


class Category(BaseModel):
    id: int
    name: str


class CustomFieldDetail(BaseModel):
    field: str
    value: str | None
    field_format: str | None = Field(None, alias="field_format")


class Component(BaseModel):
    id: int
    name: str
    category: Category
    serial: str | None = None


class Accessory(BaseModel):
    id: int
    name: str
    model_number: str | None = None
    category = Category


class Asset(BaseModel):
    id: int
    name: str
    asset_tag: str
    serial: str | None
    model: AssetModel
    category: Category
    custom_fields: dict[str, CustomFieldDetail]
    notes: str | None

    components: list[Component] = []
    accessories: list[Accessory] = []

    def get_custom_field(self, field_name: str, default: Any = None) -> str | None:
        field = self.custom_fields.get(field_name)
        return field.value if field and field.value is not None else default


class UserAssetsResponse(BaseModel):
    total: int
    rows: list[Asset]
