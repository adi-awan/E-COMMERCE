from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.notification_service import (
    get_notifications,
    create_notification,
    mark_as_read,
    mark_all_read,
    delete_notification
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def notifications(
    user: Annotated[dict, Depends(admin_required)]
):
    return get_notifications()


@router.post("/")
def add_notification(
    data: dict,
    user: Annotated[dict, Depends(admin_required)]
):
    return create_notification(
        data["title"],
        data["message"],
        data["type"]
    )


@router.patch("/{notification_id}/read")
def read_notification(
    notification_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return mark_as_read(notification_id)


@router.patch("/read-all")
def read_all(
    user: Annotated[dict, Depends(admin_required)]
):
    return mark_all_read()


@router.delete("/{notification_id}")
def remove_notification(
    notification_id: str,
    user: Annotated[dict, Depends(admin_required)]
):
    return delete_notification(notification_id)