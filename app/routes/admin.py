from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.admin_service import (
    dashboard_stats,
    recent_orders,
    low_stock_products
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