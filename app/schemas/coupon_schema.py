from pydantic import BaseModel
from typing import Optional


class CouponCreate(BaseModel):
    code: str
    discount_percent: int
    active: bool = True


class CouponApply(BaseModel):
    code: str