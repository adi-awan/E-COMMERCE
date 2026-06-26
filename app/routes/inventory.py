from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.inventory_service import (
    get_inventory,
    low_stock_products,
    update_stock
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get("/")
def inventory(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_inventory()


@router.get("/low-stock")
def low_stock(
    user: Annotated[dict, Depends(admin_required)]
):
    return low_stock_products()


@router.patch("/{product_id}")
def change_stock(
    product_id: str,
    quantity: int,
    user: Annotated[dict, Depends(admin_required)]
):
    return update_stock(
        product_id,
        quantity
    )