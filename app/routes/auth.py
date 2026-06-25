from fastapi import APIRouter, HTTPException

from app.schemas.user_schema import (
    UserCreate,
    UserLogin
)
from app.schemas.user_schema import (
    ForgotPassword,
    ResetPassword
)

from app.services.auth_service import (
    forgot_password,
    reset_password
)

from app.services.auth_service import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



@router.post("/register")
def register(
    user: UserCreate
):

    return register_user(
        user.model_dump()
    )



@router.post("/login")
def login(
    user: UserLogin
):

    result = login_user(
        user.email,
        user.password
    )


    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    return result
@router.post("/forgot-password")
def forgot(
    data: ForgotPassword
):

    return forgot_password(
        data.email
    )



@router.post("/reset-password")
def reset(
    data: ResetPassword
):

    return reset_password(
        data.token,
        data.new_password
    )