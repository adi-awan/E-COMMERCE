from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.dependencies import get_current_user

from app.schemas.profile_schema import (
    ProfileUpdate,
    PasswordUpdate
)

from app.services.profile_service import (
    get_profile,
    update_profile,
    change_password
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/")
def profile(
    user: Annotated[dict, Depends(get_current_user)]
):
    return get_profile(
        user["id"]
    )


@router.put("/")
def edit_profile(
    data: ProfileUpdate,
    user: Annotated[dict, Depends(get_current_user)]
):
    return update_profile(
        user["id"],
        data.model_dump(exclude_none=True)
    )


@router.put("/change-password")
def update_password(
    data: PasswordUpdate,
    user: Annotated[dict, Depends(get_current_user)]
):
    return change_password(
        user["id"],
        data.old_password,
        data.new_password
    )