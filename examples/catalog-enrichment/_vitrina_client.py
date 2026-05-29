"""Тонкая обёртка над 1С-Битрикс БУС REST через входящий webhook."""

from __future__ import annotations

import base64
from collections.abc import AsyncIterator
from typing import Any

import httpx


class VitrinaApiError(RuntimeError):
    """БУС REST вернул error в теле ответа."""

    def __init__(self, error: Any, description: Any = "") -> None:
        self.error = error
        self.description = description
        super().__init__(f"Bitrix REST error {error}: {description}")


class VitrinaBusClient:
    """Клиент БУС REST через incoming webhook (без OAuth).

    base — URL вида https://portal/rest/USER_ID/TOKEN (без конечного метода).
    _transport — для smoke-тестов через httpx.ASGITransport.
    """

    def __init__(
        self,
        webhook_url: str,
        iblock_id: int,
        storage_id: int,
        timeout: float = 30.0,
        _transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._base = webhook_url.rstrip("/")
        self._iblock_id = iblock_id
        self._storage_id = storage_id
        self._http = httpx.AsyncClient(timeout=timeout, transport=_transport)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def _call(self, method: str, params: dict[str, Any]) -> Any:
        """POST {base}/{method}.json — все методы БУС возвращают {result, error?}."""
        resp = await self._http.post(f"{self._base}/{method}.json", json=params)
        resp.raise_for_status()
        body = resp.json()
        if "error" in body:
            raise VitrinaApiError(body.get("error"), body.get("error_description"))
        return body["result"]

    async def list_elements(self, start: int = 0) -> list[dict[str, Any]]:
        """iblock.element.get с фильтром по IBLOCK_ID + базовые поля и свойства."""
        params = {
            "IBLOCK_ID": self._iblock_id,
            "select": ["ID", "NAME", "CODE", "XML_ID", "PROPERTY_VALUES"],
            "start": start,
        }
        result = await self._call("iblock.element.get", params)
        return list(result)

    async def iter_all_elements(self, page_size: int = 50) -> AsyncIterator[dict[str, Any]]:
        """Постранично прокачивает все элементы (БУС использует start-offset)."""
        start = 0
        while True:
            batch = await self.list_elements(start=start)
            if not batch:
                break
            for el in batch:
                yield el
            if len(batch) < page_size:
                break
            start += len(batch)

    async def upload_file(self, file_content: bytes, file_name: str) -> int:
        """disk.folder.uploadfile → ID объекта Disk-модуля."""
        b64 = base64.b64encode(file_content).decode("ascii")
        result = await self._call(
            "disk.folder.uploadfile",
            {
                "id": self._storage_id,
                "data": {"NAME": file_name},
                "fileContent": [file_name, b64],
            },
        )
        return int(result["ID"])

    async def update_element(
        self,
        element_id: int,
        *,
        detail_text: str | None = None,
        detail_picture_id: int | None = None,
    ) -> None:
        fields: dict[str, Any] = {}
        if detail_text is not None:
            fields["DETAIL_TEXT"] = detail_text
            fields["DETAIL_TEXT_TYPE"] = "text"
        if detail_picture_id is not None:
            fields["DETAIL_PICTURE"] = detail_picture_id
        if fields:
            await self._call(
                "iblock.element.update",
                {"ELEMENT_ID": element_id, "IBLOCK_ID": self._iblock_id, "FIELDS": fields},
            )

    async def set_properties(self, element_id: int, property_values: dict[str, Any]) -> None:
        """iblock.element.property.set — характеристики и галерея."""
        await self._call(
            "iblock.element.property.set",
            {
                "ELEMENT_ID": element_id,
                "IBLOCK_ID": self._iblock_id,
                "PROPERTY_VALUES": property_values,
            },
        )
