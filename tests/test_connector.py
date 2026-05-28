"""Тесты skeleton OzonConnector — все методы должны поднимать NotImplementedError."""

from decimal import Decimal

import pytest

from intelbit_river_connector_ozon.connector import OzonConnector
from intelbit_river_connector_ozon.models import OzonPrice, OzonStock


@pytest.fixture
def connector() -> OzonConnector:
    return OzonConnector(config={"client_id": "12345", "api_key": "test-key"})


class TestOzonConnectorStubs:
    @pytest.mark.asyncio
    async def test_list_orders_raises(self, connector: OzonConnector) -> None:
        with pytest.raises(NotImplementedError):
            await connector.list_orders(since="2026-05-01T00:00:00Z")

    @pytest.mark.asyncio
    async def test_ship_order_raises(self, connector: OzonConnector) -> None:
        with pytest.raises(NotImplementedError):
            await connector.ship_order("12345678-0001-1", packages=[])

    @pytest.mark.asyncio
    async def test_update_stocks_raises(self, connector: OzonConnector) -> None:
        stocks = [OzonStock(offer_id="SKU-001", warehouse_id=22222, stock=100)]
        with pytest.raises(NotImplementedError):
            await connector.update_stocks(stocks)

    @pytest.mark.asyncio
    async def test_update_prices_raises(self, connector: OzonConnector) -> None:
        prices = [OzonPrice(offer_id="SKU-001", price=Decimal("999.00"))]
        with pytest.raises(NotImplementedError):
            await connector.update_prices(prices)

    @pytest.mark.asyncio
    async def test_get_product_info_raises(self, connector: OzonConnector) -> None:
        with pytest.raises(NotImplementedError):
            await connector.get_product_info("SKU-001")

    @pytest.mark.asyncio
    async def test_health_check_raises(self, connector: OzonConnector) -> None:
        with pytest.raises(NotImplementedError):
            await connector.health_check()

    def test_config_stored(self, connector: OzonConnector) -> None:
        assert connector.config["client_id"] == "12345"
        assert connector.BASE_URL == "https://api-seller.ozon.ru"


class TestOzonAuth:
    def test_headers(self) -> None:
        from intelbit_river_connector_ozon.auth import OzonAuth

        auth = OzonAuth(client_id="12345", api_key="secret-key")
        headers = auth.headers()
        assert headers["Client-Id"] == "12345"
        assert headers["Api-Key"] == "secret-key"
        assert headers["Content-Type"] == "application/json"
