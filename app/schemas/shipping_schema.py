from pydantic import BaseModel
from typing import Optional
from datetime import date


class ShippingCreate(BaseModel):
    order_id: str
    tracking_number: Optional[str] = None
    courier: Optional[str] = None
    status: str = "Pending"
    estimated_delivery: Optional[date] = None


class ShippingUpdate(BaseModel):
    tracking_number: Optional[str] = None
    courier: Optional[str] = None
    status: Optional[str] = None
    estimated_delivery: Optional[date] = None