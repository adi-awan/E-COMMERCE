from pydantic import BaseModel


class WishlistItemCreate(BaseModel):
    product_id: str