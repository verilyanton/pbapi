from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
