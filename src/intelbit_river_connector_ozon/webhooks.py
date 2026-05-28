"""Webhook-receiver для push-уведомлений Ozon (stub)."""

from typing import Any


class OzonWebhookReceiver:
    """Приём push-уведомлений от Ozon (новые заказы, смены статусов).

    Stub — реализация в фазе 4 MVP.
    Ozon шлёт POST на настроенный URL в личном кабинете.
    """

    def __init__(self, secret: str) -> None:
        self.secret = secret

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """Проверка подписи входящего уведомления от Ozon."""
        raise NotImplementedError

    async def handle(self, message_type: str, payload: dict[str, Any]) -> None:
        """Обработка входящего push-уведомления."""
        raise NotImplementedError
