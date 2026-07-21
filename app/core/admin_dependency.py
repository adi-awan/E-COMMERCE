from fastapi import HTTPException, Depends
from typing import Annotated
from app.core.dependencies import get_current_user


def get_admin(
    user: Annotated[dict, Depends(get_current_user)]
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user