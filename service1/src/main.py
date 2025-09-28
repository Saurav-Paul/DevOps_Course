from fastapi import FastAPI

from .routes.cleanup import router as cleanup_router
from .routes.health import router as health_router
from .routes.log import router as log_router
from .routes.status import router as status_router

app = FastAPI()

app.include_router(status_router)
app.include_router(log_router)
app.include_router(cleanup_router)
app.include_router(health_router)
