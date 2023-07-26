from pydantic import BaseModel
from typing import Optional

class BookResponse(BaseModel):
    id: int
    name: str
    author: str
    publisher: str 
    price: float
    
class BookCreate(BaseModel):
    name: str
    author: str
    publisher: str
    price: float


class IdResponse(BaseModel):
    id:int
    message: Optional[str] = "Operation completed successfully."