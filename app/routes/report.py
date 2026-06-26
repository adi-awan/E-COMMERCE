from fastapi import APIRouter, Depends
from typing import Annotated

from app.core.roles import admin_required

from app.services.report_service import sales_report


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)



@router.get("/sales")
def sales(
    user: Annotated[
        dict,
        Depends(admin_required)
    ]
):

    return sales_report()