from typing import Dict
from dataclasses import dataclass

@dataclass
class Accessory:
    category: Dict[str, str]
    name: str
    model_number: str
