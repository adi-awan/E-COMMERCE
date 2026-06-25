from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.dependencies import get_current_user

from app.schemas.wishlist_schema import (
    WishlistItemCreate
)

from app.services.wishlist_service import (
    get_wishlist,
    add_to_wishlist,
    remove_from_wishlist
)

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)


@router.get("/")
def view_wishlist(
    user: Annotated[dict, Depends(get_current_user)]
):

    return get_wishlist(
        user["id"]
    )


@router.post("/add")
def add_item(
    item: WishlistItemCreate,
    user: Annotated[dict, Depends(get_current_user)]
):

    return add_to_wishlist(
        user["id"],
        item.product_id
    )


@router.delete("/{item_id}")
def delete_item(
    item_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):

    return remove_from_wishlist(
        item_id
    )