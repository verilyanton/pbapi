from pydantic import BaseModel
from typing import List


class Vendor(BaseModel):
    name: str
    products: List[str]
    owner_id: int
