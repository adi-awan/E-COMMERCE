from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.admin_review_service import (
    get_all_reviews,
    get_review_stats,
    delete_review
)

router = APIRouter(
    prefix="/admin/reviews",
    tags=["Admin Reviews"]
)


@router.get("/")
def reviews(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_all_reviews()


@router.get("/stats")
def stats(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_review_stats()


@router.delete("/{review_id}")
def remove_review(
    review_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return delete_review(review_id)