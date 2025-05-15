"""
External API integration module

Exports the hardware client as the main interface
"""
from .base_api_client import BaseAPIClient
from .hardware_client import HardwareClient
from .accessories_client import AccessoriesClient

__all__ = ['BaseAPIClient','HardwareClient', 'AccessoriesClient']