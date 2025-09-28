from __future__ import annotations

import os
from typing import Optional

import httpx

DEFAULT_STORAGE_URL = "http://storage:8080"
DEFAULT_SERVICE2_URL = "http://service2:8081"


def _storage_base_url() -> str:
    return (os.getenv("STORAGE_URL") or DEFAULT_STORAGE_URL).rstrip("/")


def _service2_status_url() -> str:
    base = os.getenv("SERVICE2_URL") or DEFAULT_SERVICE2_URL
    return f"{base.rstrip('/')}/status"


def _storage_log_url() -> str:
    return f"{_storage_base_url()}/log"


def _storage_cleanup_url() -> str:
    return f"{_storage_base_url()}/cleanup"


async def post_log_record(record: str, client: Optional[httpx.AsyncClient] = None) -> None:
    if client is None:
        async with httpx.AsyncClient() as standalone_client:
            await post_log_record(record, client=standalone_client)
            return

    await client.post(
        _storage_log_url(),
        content=record,
        headers={"Content-Type": "text/plain"},
        timeout=10.0,
    )


async def fetch_service2_status(client: Optional[httpx.AsyncClient] = None) -> str:
    if client is None:
        async with httpx.AsyncClient() as standalone_client:
            return await fetch_service2_status(client=standalone_client)

    response = await client.get(_service2_status_url(), timeout=10.0)
    response.raise_for_status()
    return response.text


async def fetch_storage_logs() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(_storage_log_url(), timeout=10.0)
        response.raise_for_status()
        return response.text


async def trigger_storage_cleanup(client: Optional[httpx.AsyncClient] = None) -> None:
    if client is None:
        async with httpx.AsyncClient() as standalone_client:
            await trigger_storage_cleanup(client=standalone_client)
            return

    response = await client.post(_storage_cleanup_url(), timeout=10.0)
    response.raise_for_status()
