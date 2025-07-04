from assets_term_generator.core.config_manager import API_HARDWARE_URL

from .base_api_client import BaseAPIClient


class HardwareClient(BaseAPIClient):
    """
    Cliente para interagir com os endpoints de /hardware da API do Snipe-IT.
    Atualmente não utilizado no fluxo principal, mas mantido para futuras funcionalidades
    como busca por asset tag ou serial.
    """

    def __init__(self) -> None:
        super().__init__(base_url=API_HARDWARE_URL)
        pass
