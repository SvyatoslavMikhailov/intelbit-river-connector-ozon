"""Управление ценами на Ozon (stub)."""

from typing import Any

from intelbit_river_connector_ozon.models import OzonPrice


class OzonPricesClient:
    """Клиент для обновления цен Ozon.

    Stub — реализация в фазе 4 MVP.
    """

    def __init__(self, base_url: str, auth_headers: dict[str, str]) -> None:
        self.base_url = base_url
        self.auth_headers = auth_headers

    async def update(self, prices: list[OzonPrice]) -> dict[str, Any]:
        """POST /v1/product/import/prices — обновить цены товаров."""
        raise NotImplementedError

    async def get_info(self, offer_ids: list[str]) -> list[OzonPrice]:
        """Получить текущие цены по списку offer_id."""
        raise NotImplementedError
