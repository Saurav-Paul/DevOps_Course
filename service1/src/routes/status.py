from fastapi import APIRouter, Response
from fastapi.concurrency import run_in_threadpool
import httpx

from ..services.metrics import build_status_record
from ..services.vstorage import append_to_vstorage
from ..services.storage_client import post_log_record, fetch_service2_status

router = APIRouter()

@router.get("/status", response_class=Response)
async def get_status() -> Response:
    record = await run_in_threadpool(build_status_record)

    await run_in_threadpool(append_to_vstorage, record)

    async with httpx.AsyncClient() as client:
        await post_log_record(record, client=client)
        service2_status = await fetch_service2_status(client=client)

    return Response(
        content=f"{record}\n{service2_status.rstrip()}",
        media_type="text/plain",
    )
