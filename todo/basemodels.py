from pydantic import BaseModel,conint, confloat
from typing import Optional

class BookQuery(BaseModel):
    limit: conint(ge=1) = 10
    offset: conint(ge=0) = 0
    name: str 
    author: str 
    publisher: str 
    price_min: confloat(ge=0.0) = None
    price_max: confloat(ge=100.0) = None

class BookResponse(BaseModel):
    id: int
    name: str
    author: str
    publisher: str 
    price: float
    message: Optional[str] = "Operation completed successfully."
    
class BookCreate(BaseModel):
    name: str
    author: str
    publisher: str
    price: float
    message: Optional[str] = "Operation completed successfully."


class IdResponse(BaseModel):
    id:int
    message: Optional[str] = "Operation completed successfully."