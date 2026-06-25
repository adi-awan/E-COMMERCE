from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.dependencies import get_current_user

from app.services.payment_service import (
    create_payment,
    verify_payment
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/{order_id}")
def pay_order(
    order_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):
    return create_payment(order_id)


@router.post("/verify/{order_id}")
def confirm_payment(
    order_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):
    return verify_payment(order_id)