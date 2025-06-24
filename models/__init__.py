"""
System data models definitions

Exports Asset class as the main interface
"""

from .accessory import Accessory
from .asset import Asset, AssetList

__all__ = ["Asset", "AssetList", "Accessory"]
