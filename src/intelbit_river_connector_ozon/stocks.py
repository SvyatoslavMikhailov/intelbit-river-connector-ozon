"""Управление остатками на складах Ozon (stub)."""

from typing import Any

from intelbit_river_connector_ozon.models import OzonStock


class OzonStocksClient:
    """Клиент для обновления остатков Ozon.

    Stub — реализация в фазе 4 MVP.
    """

    def __init__(self, base_url: str, auth_headers: dict[str, str]) -> None:
        self.base_url = base_url
        self.auth_headers = auth_headers

    async def update(self, stocks: list[OzonStock]) -> dict[str, Any]:
        """POST /v1/product/info/stocks-by-warehouse/fbs — обновить остатки."""
        raise NotImplementedError

    async def get_by_warehouse(self, warehouse_id: int) -> list[OzonStock]:
        """Получить текущие остатки по складу."""
        raise NotImplementedError
