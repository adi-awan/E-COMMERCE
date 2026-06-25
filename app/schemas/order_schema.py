from pydantic import BaseModel


class OrderCreate(BaseModel):
    pass


class OrderStatusUpdate(BaseModel):
    status: str