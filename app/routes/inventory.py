from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.inventory_service import (
    low_stock_products
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get("/low-stock")
def low_stock(
    user: Annotated[dict, Depends(admin_required)]
):

    return low_stock_products()