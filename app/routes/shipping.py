from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.schemas.shipping_schema import (
    ShippingCreate,
    ShippingUpdate
)

from app.services.shipping_service import (
    get_all_shipments,
    get_shipping,
    create_shipping,
    update_shipping,
    delete_shipping
)

router = APIRouter(
    prefix="/shipping",
    tags=["Shipping"]
)


@router.get("/")
def shipments(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_all_shipments()


@router.get("/{order_id}")
def shipment(
    order_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return get_shipping(order_id)


@router.post("/")
def create(
    shipping: ShippingCreate,
    user: Annotated[dict, Depends(admin_required)]
):
    return create_shipping(
        shipping.model_dump()
    )


@router.put("/{shipping_id}")
def update(
    shipping_id: str,
    shipping: ShippingUpdate,
    user: Annotated[dict, Depends(admin_required)]
):
    return update_shipping(
        shipping_id,
        shipping.model_dump(exclude_none=True)
    )


@router.delete("/{shipping_id}")
def delete(
    shipping_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return delete_shipping(shipping_id)