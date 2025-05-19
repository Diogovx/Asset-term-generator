"""
External API integration module

Exports the hardware client as the main interface
"""
from .accessories_client import AccessoriesClient
from .base_api_client import BaseAPIClient
from .hardware_client import HardwareClient

__all__ = ['BaseAPIClient','HardwareClient', 'AccessoriesClient']