from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.core.roles import admin_required

from app.schemas.coupon_schema import (
    CouponCreate,
    CouponApply
)

from app.services.coupon_service import (
    create_coupon,
    get_coupon,
    get_all_coupons
)

router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"]
)


@router.get("/")
def list_coupons(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_all_coupons()


@router.post("/")
def add_coupon(
    coupon: CouponCreate,
    user: Annotated[dict, Depends(admin_required)]
):
    return create_coupon(
        coupon.model_dump()
    )


@router.post("/validate")
def validate_coupon(
    data: CouponApply
):

    coupon = get_coupon(
        data.code
    )

    if not coupon:
        raise HTTPException(
            status_code=404,
            detail="Invalid coupon"
        )

    return coupon