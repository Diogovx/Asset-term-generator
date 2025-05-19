from dataclasses import dataclass


@dataclass
class Accessory:
    category: dict[str, str]
    name: str
    model_number: str
