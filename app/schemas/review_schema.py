from pydantic import BaseModel


class ReviewCreate(BaseModel):
    product_id: str
    rating: int
    comment: str


class ReviewUpdate(BaseModel):
    rating: int
    comment: str