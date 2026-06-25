from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.dependencies import get_current_user

from app.schemas.review_schema import (
    ReviewCreate,
    ReviewUpdate
)

from app.services.review_service import (
    get_reviews,
    add_review,
    update_review,
    delete_review
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.get("/{product_id}")
def product_reviews(
    product_id: str
):
    return get_reviews(
        product_id
    )


@router.post("/")
def create_review(
    review: ReviewCreate,
    user: Annotated[dict, Depends(get_current_user)]
):
    return add_review(
        user["id"],
        review.model_dump()
    )


@router.put("/{review_id}")
def edit_review(
    review_id: str,
    review: ReviewUpdate,
    user: Annotated[dict, Depends(get_current_user)]
):
    return update_review(
        review_id,
        review.model_dump()
    )


@router.delete("/{review_id}")
def remove_review(
    review_id: str,
    user: Annotated[dict, Depends(get_current_user)]
):
    return delete_review(
        review_id
    )