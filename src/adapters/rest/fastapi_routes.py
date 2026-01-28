import time
from typing import Optional

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from src.helpers.common import get_logger

from src.handlers.add_barcodes import add_barcodes_handler
from src.handlers.link_shop import link_shop_handler
from src.handlers.parse_from_url import parse_from_url_handler
from src.handlers.shops import shops_handler
from src.handlers.user_identity import UserIdentityHandler
from src.schemas.request_schemas import (
    ParseFromUrlRequest,
    LinkShopRequest,
    AddBarcodesRequest,
    GetOrCreateUserByIdentityRequest,
)
from src.schemas.response_schemas import Health

HomeRouter = APIRouter(tags=["home"])
HealthRouter = APIRouter(prefix="/health", tags=["health"])
UserRouter = APIRouter(prefix="/user", tags=["user"])


@HomeRouter.get("/", response_model=Health)
async def home(request: Request, logger=Depends(get_logger)):
    logger.info("Home endpoint called")
    return await health(request, logger)


@HealthRouter.get("", response_model=Health)
async def health(request: Request, logger=Depends(get_logger)):
    logger.info("Health endpoint called")
    return Health()


@HealthRouter.get("/deep-ping", response_model=Health)
async def deep_ping(request: Request, logger=Depends(get_logger)):
    logger.info("Deep ping endpoint called")
    time.sleep(1)
    return Health()


@UserRouter.post("/get-or-create-by-identity")
async def get_or_create_user_by_identity(
    request: GetOrCreateUserByIdentityRequest, logger=Depends(get_logger)
):
    logger.info(f"User identity: {request.id} for provider: {request.provider}")
    handler = UserIdentityHandler(logger)
    user = handler.get_or_create_user_by_identity(
        request.id, request.provider, request.email, request.name
    )
    return user


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
#
#
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return Response(status_code=204)
#
#
# @app.get("/openapi.json", include_in_schema=False)
# async def get_openapi():
#     return app.openapi()
#
#
# @app.post("/parse")
# @app.post("/parse-from-url")
# async def parse_from_url(request: ParseFromUrlRequest):
#     status, response = parse_from_url_handler(request.url, request.user_id, logger)
#     return JSONResponse(content=response, status_code=status.value)
#
#
# @app.post("/link-shop")
# async def link_shop(request: LinkShopRequest):
#     status, response = link_shop_handler(
#         request.url, request.user_id, request.receipt_id, logger
#     )
#     return JSONResponse(content=response, status_code=status.value)
#
#
# @app.post("/add-barcodes")
# async def add_barcodes(request: AddBarcodesRequest):
#     status, response = add_barcodes_handler(request.shop_id, request.items, logger)
#     return JSONResponse(content=response, status_code=status.value)
#
#
# @app.get("/shops")
# async def get_shops(
#     request: Request,
#     country_code: Optional[str] = None,
#     company_id: Optional[str] = None,
#     lat_min: Optional[float] = None,
#     lat_max: Optional[float] = None,
#     lon_min: Optional[float] = None,
#     lon_max: Optional[float] = None,
#     limit: Optional[int] = 50,
#     offset: Optional[int] = 0,
# ):
#     query_params = {}
#     if country_code:
#         query_params["country_code"] = country_code
#     if company_id:
#         query_params["company_id"] = company_id
#     if lat_min is not None:
#         query_params["lat_min"] = lat_min
#     if lat_max is not None:
#         query_params["lat_max"] = lat_max
#     if lon_min is not None:
#         query_params["lon_min"] = lon_min
#     if lon_max is not None:
#         query_params["lon_max"] = lon_max
#     query_params["limit"] = limit
#     query_params["offset"] = offset
#
#     status, response = shops_handler(query_params, logger)
#     return JSONResponse(content=response, status_code=status.value)
