
from pydantic import BaseModel, Field


class CustomFieldDetail(BaseModel):
    field: str
    value: str | None = None
    field_format: str | None = Field(None, alias='field_format')
    element: str | None = None


class Asset(BaseModel):
    asset_id: int
    asset_tag: str
    serial: str | None
    model: str
    category: str
    custom_fields: dict[str, CustomFieldDetail]
    
    def get_custom_field(self, field_name: str, default: str | None = None) -> str | None:
        field = self.custom_fields.get(field_name)
        return field.value if field else default

class UserAssetsResponse(BaseModel):
    assets: list[Asset]
    user_id: int
    user_name: str
    employee_number: str
