from fastapi import APIRouter, Response

from ..services.storage_client import fetch_storage_logs

router = APIRouter()

@router.get("/log", response_class=Response)
async def get_log() -> Response:
    logs = await fetch_storage_logs()
    return Response(content=logs, media_type="text/plain")
