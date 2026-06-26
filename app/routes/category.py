from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate
)

from app.services.category_service import (
    get_categories,
    create_category,
    update_category,
    delete_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/")
def all_categories(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_categories()


@router.post("/")
def add_category(
    category: CategoryCreate,
    user: Annotated[dict, Depends(admin_required)]
):
    return create_category(
        category.model_dump()
    )


@router.put("/{category_id}")
def edit_category(
    category_id: str,
    category: CategoryUpdate,
    user: Annotated[dict, Depends(admin_required)]
):
    return update_category(
        category_id,
        category.model_dump(exclude_none=True)
    )


@router.delete("/{category_id}")
def remove_category(
    category_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return delete_category(category_id)