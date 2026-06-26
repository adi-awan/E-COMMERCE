from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    image: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None