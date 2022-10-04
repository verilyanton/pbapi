from pydantic import BaseModel


class Health(BaseModel):
    message: str = "Plant-Based API is healthy"
