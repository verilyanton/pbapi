import time
from fastapi import APIRouter

from src.schemas.health import Health

HealthRouter = APIRouter(
    prefix="/health",
    tags=["health"]
)


@HealthRouter.get("")
async def get():
    return Health()


@HealthRouter.get("/deep-ping")
async def deep_ping():
    time.sleep(1)
    return Health()
