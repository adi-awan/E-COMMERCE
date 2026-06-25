from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.dependencies import get_current_user
from app.core.roles import admin_required

from app.schemas.checkout_schema import CheckoutRequest
from app.schemas.order_status_schema import OrderStatusUpdate

from app.services.order_service import (
    checkout,
    get_orders,
    get_order,
    track_order,
    get_all_orders,
    update_order_status
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# Customer Checkout
@router.post("/checkout")
def create_order(
    data: CheckoutRequest,
    user: Annotated[dict, Depends(get_current_user)]
):

    return checkout(
        user["id"],
        data.coupon_code
    )


# Customer Order History
@router.get("/")
def order_history(
    user: Annotated[dict, Depends(get_current_user)]
):

    return get_orders(
        user["id"]
    )


# Get Single Order Details
@router.get("/{order_id}")
def order_details(
    order_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):

    return get_order(
        order_id
    )


# Track Order
@router.get("/track/{order_id}")
def track(
    order_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):

    return track_order(
        order_id
    )


# Admin: Get All Orders
@router.get("/admin/all")
def admin_orders(
    user: Annotated[dict, Depends(admin_required)]
):

    return get_all_orders()


# Admin: Update Order Status
@router.put("/admin/{order_id}")
def change_status(
    order_id: str,
    data: OrderStatusUpdate,
    user: Annotated[dict, Depends(admin_required)]
):

    return update_order_status(
        order_id,
        data.status
    )