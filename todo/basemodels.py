from pydantic import BaseModel


class BookResponse(BaseModel):
    id: int
    name: str
    publisher: str 
    author: str
    price: float
    
class BookCreate(BaseModel):
    name: str
    author: str
    publisher: str
    price: float


class IdResponse(BaseModel):
    id:int