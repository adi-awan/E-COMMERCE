from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required
from app.schemas.order_schema import OrderStatusUpdate
from app.services.admin_service import (
    dashboard_stats,
    recent_orders,
    low_stock_products,
    get_all_users,
    get_user,
    update_user_role,
    delete_user,
    get_all_reviews,
    review_statistics,
    admin_delete_review
)
from app.services.order_service import (
    get_all_orders,
    get_order,
    update_order_status,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)


@router.get("/stats")
def stats(
    user: Annotated[dict, Depends(admin_required)]
):
    return dashboard_stats()


@router.get("/recent-orders")
def latest_orders(
    user: Annotated[dict, Depends(admin_required)]
):
    return recent_orders()


@router.get("/low-stock")
def low_stock(
    user: Annotated[dict, Depends(admin_required)]
):
    return low_stock_products()


@router.get("/orders")
def all_orders(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_all_orders()


@router.get("/orders/{order_id}")
def order(
    order_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return get_order(order_id)


@router.put("/orders/{order_id}")
def change_status(
    order_id: str,
    data: OrderStatusUpdate,
    user: Annotated[dict, Depends(admin_required)]
):
    return update_order_status(
        order_id,
        data.status
    )


@router.delete("/orders/{order_id}")
def remove_order(
    order_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return delete_order(order_id)

@router.get("/users")
def users(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_all_users()


@router.get("/users/{user_id}")
def single_user(
    user_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return get_user(user_id)


@router.put("/users/{user_id}")
def change_role(
    user_id: str,
    data: dict,
    user: Annotated[dict, Depends(admin_required)]
):
    return update_user_role(
        user_id,
        data["role"]
    )


@router.delete("/users/{user_id}")
def remove_user(
    user_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return delete_user(user_id)
@router.get("/reviews")
def all_reviews(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_all_reviews()


@router.get("/reviews/stats")
def review_stats(
    user: Annotated[dict, Depends(admin_required)]
):
    return review_statistics()


@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return admin_delete_review(review_id)