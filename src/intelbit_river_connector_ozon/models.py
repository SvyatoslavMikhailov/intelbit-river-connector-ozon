"""Pydantic-модели Ozon Seller API."""

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class FulfillmentType(StrEnum):
    fbs = "fbs"
    fbo = "fbo"
    rfbs = "rfbs"


class PostingStatus(StrEnum):
    awaiting_packaging = "awaiting_packaging"
    awaiting_deliver = "awaiting_deliver"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"


class OzonProduct(BaseModel):
    """Товар в каталоге Ozon."""

    offer_id: str
    product_id: int = 0
    name: str
    sku: int = 0
    barcode: str = ""
    is_archived: bool = False


class OzonStock(BaseModel):
    """Остаток товара на складе Ozon."""

    offer_id: str
    warehouse_id: int
    stock: int
    reserved: int = 0


class OzonPrice(BaseModel):
    """Цена товара на Ozon."""

    offer_id: str
    price: Decimal
    old_price: Decimal = Decimal("0")
    min_price: Decimal = Decimal("0")
    currency_code: str = "RUB"


class PostingProduct(BaseModel):
    """Товарная позиция в отправлении."""

    sku: int
    name: str
    offer_id: str
    quantity: int
    price: str
    currency_code: str = "RUB"


class OzonPosting(BaseModel):
    """Отправление (заказ) Ozon FBS."""

    posting_number: str
    order_id: int
    order_number: str
    status: PostingStatus
    fulfillment_type: FulfillmentType = FulfillmentType.fbs
    created_at: str
    in_process_at: str = ""
    products: list[PostingProduct] = Field(default_factory=list)
    tracking_number: str = ""
    warehouse_id: int = 0
