from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.vendor import Vendor

VendorRouter = APIRouter(prefix="/vendors", tags=["vendors"])

# A list to store our vendors (mock database for now)
vendors: List[Vendor] = []


@VendorRouter.post("/")
async def add_vendor(vendor: Vendor):
    vendors.append(vendor)
    return {"name": vendor.name, "products": vendor.products}


@VendorRouter.get("/")
async def read_vendors():
    return {"vendors": vendors}


@VendorRouter.get("/{vendor_name}")
async def read_vendor(vendor_name: str):
    for vendor in vendors:
        if vendor.name == vendor_name:
            return {"name": vendor.name, "products": vendor.products}
    raise HTTPException(status_code=404, detail="Vendor not found")
