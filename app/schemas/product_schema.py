from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    image: Optional[str] = None
    stock: int = 0


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    stock: Optional[int] = None