from pydantic import BaseModel
from typing import Optional


class CheckoutRequest(BaseModel):
    coupon_code: Optional[str] = None