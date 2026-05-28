"""OzonConnector — коннектор Ozon Seller API для Интелбит:Река.

Реализует контракт Connector из intelbit-river-sdk (ADR-006).
Стадия: skeleton (v0.0.1). Реализация — фаза 4 MVP.
"""

from typing import Any

from intelbit_river_connector_ozon.models import OzonPosting, OzonPrice, OzonStock


class OzonConnector:
    """Коннектор Ozon Seller API (FBS-сценарий).

    Поддерживает FBS — главный сценарий для торговых компаний (Cyberflot).
    Все методы — NotImplementedError. Реализация в фазе 4.
    """

    BASE_URL = "https://api-seller.ozon.ru"

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    async def list_orders(self, since: str, status: str | None = None) -> list[OzonPosting]:
        """Список заказов FBS через POST /v3/posting/fbs/list."""
        raise NotImplementedError

    async def ship_order(self, posting_number: str, packages: list[dict[str, Any]]) -> bool:
        """Отгрузить заказ через POST /v3/posting/fbs/ship."""
        raise NotImplementedError

    async def update_stocks(self, stocks: list[OzonStock]) -> dict[str, Any]:
        """Push остатков через POST /v1/product/info/stocks-by-warehouse/fbs."""
        raise NotImplementedError

    async def update_prices(self, prices: list[OzonPrice]) -> dict[str, Any]:
        """Push цен через POST /v1/product/import/prices."""
        raise NotImplementedError

    async def get_product_info(self, offer_id: str) -> dict[str, Any]:
        """Информация о товаре по offer_id."""
        raise NotImplementedError

    async def health_check(self) -> bool:
        """Проверка доступности Ozon API."""
        raise NotImplementedError
