"""FastAPI-мок Ozon Seller API.

Имитирует 7 endpoints Ozon (все POST + JSON), проверяет auth-заголовки
(Client-Id + Api-Key) и симулирует rate-limit: 6-й запрос к любому endpoint
возвращает 429 + Retry-After: 1 (для проверки backoff в OzonRateLimiter).

create_app() возвращает СВЕЖЕЕ приложение с обнулёнными счётчиками — каждый
contract-тест берёт изолированный экземпляр (иначе счётчики 429 текут между тестами).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

_RATE_LIMIT_AT = 6  # на каком по счёту запросе к endpoint вернуть 429

_POSTINGS: list[dict[str, Any]] = [
    {
        "posting_number": f"12345678-000{i}-1",
        "order_id": 111000 + i,
        "order_number": f"12345678-000{i}",
        "status": status,
        "in_process_at": "2026-05-28T10:00:00Z",
        "warehouse_id": 22222,
        "products": [
            {
                "sku": 123450 + i,
                "name": f"Care Friend товар {i}",
                "offer_id": f"CF-00{i}",
                "quantity": 1,
                "price": "1990.00",
                "currency_code": "RUB",
            }
        ],
    }
    for i, status in enumerate(
        ["awaiting_packaging", "awaiting_deliver", "delivering", "delivered", "cancelled"],
        start=1,
    )
]


def create_app() -> FastAPI:
    app = FastAPI(title="Ozon Mock Server", version="0.1.0")
    counters: dict[str, int] = defaultdict(int)

    @app.middleware("http")
    async def auth_and_rate_limit(request: Request, call_next: Any) -> Any:
        if not request.headers.get("Client-Id") or not request.headers.get("Api-Key"):
            return JSONResponse(
                status_code=401, content={"code": 401, "message": "missing auth headers"}
            )
        counters[request.url.path] += 1
        if counters[request.url.path] == _RATE_LIMIT_AT:
            return JSONResponse(
                status_code=429,
                content={"code": 429, "message": "too many requests"},
                headers={"Retry-After": "1"},
            )
        return await call_next(request)

    @app.post("/v3/posting/fbs/list")
    async def list_fbs(body: dict[str, Any]) -> dict[str, Any]:
        return {"result": {"postings": _POSTINGS, "has_next": False}}

    @app.post("/v3/posting/fbs/get")
    async def get_fbs(body: dict[str, Any]) -> dict[str, Any]:
        return {"result": _POSTINGS[0]}

    @app.post("/v3/posting/fbs/ship")
    async def ship_fbs(body: dict[str, Any]) -> dict[str, Any]:
        return {"result": [body.get("posting_number", "")]}

    @app.post("/v1/product/info/stocks-by-warehouse/fbs")
    async def update_stocks(body: dict[str, Any]) -> dict[str, Any]:
        return {
            "result": [
                {
                    "product_id": s.get("product_id", 0),
                    "offer_id": s.get("offer_id", ""),
                    "warehouse_id": s.get("warehouse_id", 0),
                    "updated": True,
                    "errors": [],
                }
                for s in body.get("stocks", [])
            ]
        }

    @app.post("/v1/product/import/prices")
    async def import_prices(body: dict[str, Any]) -> dict[str, Any]:
        return {
            "result": [
                {
                    "product_id": p.get("product_id", 0),
                    "offer_id": p.get("offer_id", ""),
                    "updated": True,
                    "errors": [],
                }
                for p in body.get("prices", [])
            ]
        }

    @app.post("/v2/product/info/stocks")
    async def get_stocks(body: dict[str, Any]) -> dict[str, Any]:
        return {
            "result": {
                "items": [
                    {
                        "product_id": 555001,
                        "offer_id": "CF-001",
                        "stocks": [{"present": 120, "reserved": 5}],
                    }
                ]
            }
        }

    @app.post("/v4/product/info/prices")
    async def get_prices(body: dict[str, Any]) -> dict[str, Any]:
        return {
            "result": {
                "items": [
                    {
                        "product_id": 555001,
                        "offer_id": "CF-001",
                        "price": {
                            "price": "1790.00",
                            "old_price": "1990.00",
                            "min_price": "1500.00",
                            "currency_code": "RUB",
                        },
                    }
                ]
            }
        }

    return app
