from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.analytics_service import (
    revenue_summary,
    top_products
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/revenue")
def revenue(
    user: Annotated[dict, Depends(admin_required)]
):
    return revenue_summary()


@router.get("/top-products")
def best_sellers(
    user: Annotated[dict, Depends(admin_required)]
):
    return top_products()