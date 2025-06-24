from dataclasses import dataclass


@dataclass
class Asset:
    category: str
    model: str
    asset_tag: str


@dataclass
class AssetList:
    user_id: str
    user_name: str
    employee_number: str
    assets: list[Asset]
