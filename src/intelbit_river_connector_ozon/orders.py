"""Работа с заказами FBS/FBO Ozon (stub)."""

from typing import Any

from intelbit_river_connector_ozon.models import OzonPosting


class OzonOrdersClient:
    """Клиент для работы с отправлениями Ozon.

    Stub — реализация в фазе 4 MVP.
    """

    def __init__(self, base_url: str, auth_headers: dict[str, str]) -> None:
        self.base_url = base_url
        self.auth_headers = auth_headers

    async def list_fbs(self, since: str, to: str, status: str | None = None) -> list[OzonPosting]:
        """POST /v3/posting/fbs/list — список FBS-отправлений за период."""
        raise NotImplementedError

    async def ship(self, posting_number: str, packages: list[dict[str, Any]]) -> bool:
        """POST /v3/posting/fbs/ship — передать заказ на доставку."""
        raise NotImplementedError

    async def cancel(self, posting_number: str, reason_id: int) -> bool:
        """POST /v3/posting/fbs/cancel — отменить отправление."""
        raise NotImplementedError
