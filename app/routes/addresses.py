from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.dependencies import get_current_user

from app.schemas.address_schema import (
    AddressCreate,
    AddressUpdate
)

from app.services.address_service import (
    get_addresses,
    add_address,
    update_address,
    delete_address
)

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)


@router.get("/")
def list_addresses(
    user: Annotated[dict, Depends(get_current_user)]
):
    return get_addresses(
        user["id"]
    )


@router.post("/")
def create_address(
    address: AddressCreate,
    user: Annotated[dict, Depends(get_current_user)]
):
    return add_address(
        user["id"],
        address.model_dump()
    )


@router.put("/{address_id}")
def edit_address(
    address_id: str,
    address: AddressUpdate,
    user: Annotated[dict, Depends(get_current_user)]
):
    return update_address(
        address_id,
        user["id"],
        address.model_dump(exclude_none=True)
    )


@router.delete("/{address_id}")
def remove_address(
    address_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):
    return delete_address(
        address_id,
        user["id"]
    )