from fastapi import APIRouter, Response
from fastapi.concurrency import run_in_threadpool

from ..services.storage_client import trigger_storage_cleanup
from ..services.vstorage import clear_vstorage

router = APIRouter()


@router.post("/cleanup", response_class=Response)
async def cleanup() -> Response:
    await run_in_threadpool(clear_vstorage)
    await trigger_storage_cleanup()
    return Response(content="Cleaned up", media_type="text/plain")
