# Особенности Ozon Seller API

Документ фиксирует нюансы, которые влияют на реализацию коннектора.

## Rate Limits

- Базовый лимит: ~1 req/s для большинства методов
- Пакетные методы (цены, остатки): до 1000 позиций за вызов, рекомендуется не чаще 1 раз/2с
- При превышении лимита: HTTP 429, Retry-After в заголовке

## Eventual Consistency

- После `update_stocks` / `update_prices` — изменения видны на сайте Ozon через 15-30 минут
- Не опрашивать остатки сразу после обновления для проверки — данные не изменятся мгновенно

## Webhook Delivery

- Ozon шлёт POST на настроенный URL в кабинете (один endpoint на всё)
- Подпись в заголовке `X-Ozon-Signature` (HMAC-SHA256, ключ = webhook_secret)
- Гарантия at-least-once: дублирующие события возможны — нужна идемпотентность

## Статусы FBS Posting

Жизненный цикл: `awaiting_packaging` → `awaiting_deliver` → `delivering` → `delivered`
Отмена возможна только из `awaiting_packaging`.

## Pagination

Методы list используют курсорную пагинацию (`last_id` / `page`). Размер страницы до 1000.
