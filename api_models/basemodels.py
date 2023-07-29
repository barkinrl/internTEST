from pydantic import BaseModel,conint, confloat
from typing import Optional


class BookCreate(BaseModel):
    name: str
    author: str
    publisher: str
    price: float


class BookQuery(BaseModel):
    limit: conint = 10
    offset: conint = 0
    name: str = None
    author: str = None
    publisher: str = None
    price_min: confloat = None
    price_max: confloat = None


class BookResponse(BaseModel):
    id: int
    name: str
    author: str
    publisher: str 
    price: float


class IdResponse(BaseModel):
    id:int
    message: Optional[str] = "Operation completed successfully."






