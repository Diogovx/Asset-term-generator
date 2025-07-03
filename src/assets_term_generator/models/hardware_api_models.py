from typing import Any

from pydantic import BaseModel, Field


class AssetModel(BaseModel):
    id: int
    name: str | None = None


class Category(BaseModel):
    id: int
    name: str | None = None


class CustomFieldDetail(BaseModel):
    field: str
    value: str | None
    field_format: str | None = Field(None, alias="field_format")


class AccessoryCheckoutTarget(BaseModel):
    id: int
    type: str
    name: str


class AccessoryCheckout(BaseModel):
    id: int
    assigned_to: AccessoryCheckoutTarget


# Modelo para cada linha na resposta de /components/{id}/assets
class ComponentAssetAssignment(BaseModel):
    id: int  # ID do ativo
    name: str
    type: str


class Component(BaseModel):
    id: int
    name: str | None = None
    category: Category | str
    serial: str | None = None
    assigned_to: int | None = None
    assigned_type: str | None = None


class Accessory(BaseModel):
    id: int
    name: str | None = None
    model_number: str | None = None
    category: Category | str
    assigned_to: int | None = None
    assigned_type: str | None = None


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
