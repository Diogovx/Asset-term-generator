"""
External API integration module

Exports the hardware client as the main interface
"""
from .hardware_client import HardwareClient
from .accessories_client import AccessoriesClient

__all__ = ['HardwareClient', 'AccessoriesClient']