"""Учёт лимитов Ozon API и retry-логика через tenacity (placeholder)."""


class OzonRateLimiter:
    """Контроль rate limits Ozon Seller API.

    Ozon документирует лимиты на уровне endpoint:
    - большинство методов: 1 req/s или 60 req/min
    - импорт цен/остатков: пакетные, до 1000 позиций за вызов

    Placeholder — интеграция с tenacity в фазе 4.
    """

    def __init__(self, requests_per_minute: int = 60) -> None:
        self.requests_per_minute = requests_per_minute

    async def acquire(self) -> None:
        """Запросить токен перед HTTP-вызовом (rate limiting)."""
        raise NotImplementedError
