from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.admin_service import (
    dashboard_stats,
    recent_orders,
    low_stock_products,
    get_all_orders,
    get_order,
    update_order_status,
    delete_order,
    get_all_users,
    get_user,
    update_user_role,
    delete_user
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
    status: dict,
    user: Annotated[dict, Depends(admin_required)]
):
    return update_order_status(
        order_id,
        status["status"]
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