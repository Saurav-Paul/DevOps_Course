from __future__ import annotations

import os
from typing import Awaitable, Callable, Optional, TypeVar

import httpx

DEFAULT_STORAGE_URL = "http://storage:8080"
DEFAULT_SERVICE2_URL = "http://service2:8081"

T = TypeVar("T")


def _storage_base_url() -> str:
    return (os.getenv("STORAGE_URL") or DEFAULT_STORAGE_URL).rstrip("/")


def _service2_base_url() -> str:
    return (os.getenv("SERVICE2_URL") or DEFAULT_SERVICE2_URL).rstrip("/")


def _service2_status_url() -> str:
    return f"{_service2_base_url()}/status"


def _service2_health_url() -> str:
    return f"{_service2_base_url()}/health"


def _storage_log_url() -> str:
    return f"{_storage_base_url()}/log"


def _storage_health_url() -> str:
    return f"{_storage_base_url()}/health"


def _storage_cleanup_url() -> str:
    return f"{_storage_base_url()}/cleanup"


async def _ensure_client(
    func: Callable[[httpx.AsyncClient], Awaitable[T]],
    client: Optional[httpx.AsyncClient],
) -> T:
    if client is not None:
        return await func(client)

    async with httpx.AsyncClient() as created_client:
        return await func(created_client)


async def post_log_record(record: str, client: Optional[httpx.AsyncClient] = None) -> None:
    async def _post(active_client: httpx.AsyncClient) -> None:
        await active_client.post(
            _storage_log_url(),
            content=record,
            headers={"Content-Type": "text/plain"},
            timeout=10.0,
        )

    await _ensure_client(_post, client)


async def fetch_service2_status(client: Optional[httpx.AsyncClient] = None) -> str:
    async def _fetch(active_client: httpx.AsyncClient) -> str:
        response = await active_client.get(_service2_status_url(), timeout=10.0)
        response.raise_for_status()
        return response.text

    return await _ensure_client(_fetch, client)


async def fetch_storage_logs() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(_storage_log_url(), timeout=10.0)
        response.raise_for_status()
        return response.text


async def trigger_storage_cleanup(client: Optional[httpx.AsyncClient] = None) -> None:
    async def _cleanup(active_client: httpx.AsyncClient) -> None:
        response = await active_client.post(_storage_cleanup_url(), timeout=10.0)
        response.raise_for_status()

    await _ensure_client(_cleanup, client)


async def is_storage_healthy(client: Optional[httpx.AsyncClient] = None) -> bool:
    async def _check(active_client: httpx.AsyncClient) -> bool:
        try:
            response = await active_client.get(_storage_health_url(), timeout=5.0)
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
        except Exception:
            return False

    return await _ensure_client(_check, client)


async def is_service2_healthy(client: Optional[httpx.AsyncClient] = None) -> bool:
    async def _check(active_client: httpx.AsyncClient) -> bool:
        try:
            response = await active_client.get(_service2_health_url(), timeout=5.0)
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
        except Exception:
            return False

    return await _ensure_client(_check, client)
