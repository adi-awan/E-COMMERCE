from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    image_url: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None