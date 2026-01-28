import logging
from fastapi import APIRouter

SearchRouter = APIRouter(
    prefix="/v1/search",
    tags=["search"],
)

logger = logging.getLogger(__name__)
