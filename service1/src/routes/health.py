import asyncio

from fastapi import APIRouter

from ..services.storage_client import is_service2_healthy, is_storage_healthy

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, bool]:
    storage_ok, service2_ok = await asyncio.gather(
        is_storage_healthy(),
        is_service2_healthy(),
    )

    return {
        "service1": True,
        "service2": service2_ok,
        "storage": storage_ok,
    }
