from fastapi import APIRouter, Depends
from typing import Annotated


from app.core.dependencies import get_current_user

from app.schemas.cart_schema import (
    CartItemCreate,
    CartItemUpdate
)

from app.services.cart_service import (
    get_cart,
    add_to_cart,
    update_cart_item,
    remove_cart_item
)



router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)



@router.get("/")
def view_cart(
    user: Annotated[dict, Depends(get_current_user)]
):

    return get_cart(
        user["id"]
    )



@router.post("/add")
def add_item(
    item: CartItemCreate,
    user: Annotated[dict, Depends(get_current_user)]
):

    return add_to_cart(
        user["id"],
        item.model_dump()
    )



@router.put("/{item_id}")
def update_item(
    item_id: str,
    item: CartItemUpdate,
    user: Annotated[dict, Depends(get_current_user)]
):

    return update_cart_item(
        user["id"],
        item_id,
        item.quantity
    )



@router.delete("/{item_id}")
def delete_item(
    item_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):

    return remove_cart_item(
        user["id"],
        item_id
    )