"""
System utilities

Exports functions to:
- Logging configuration
- Custom exceptions
- Custom error messages
"""

from .exceptions import (
    ApplicationError,
    AssetNotFoundError,
    InvalidInputError,
    NoCompatibleAssetsError,
    TemplateConfigError,
    UserNotFoundError,
)
from .logging_config import configure_logging

__all__ = [
    "configure_logging",
    "UserNotFoundError",
    "AssetNotFoundError",
    "ApplicationError",
    "InvalidInputError",
    "NoCompatibleAssetsError",
    "TemplateConfigError",
]
