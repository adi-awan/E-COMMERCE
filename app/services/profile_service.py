from fastapi import HTTPException

from app.core.supabase import supabase
from app.core.security import (
    verify_password,
    hash_password
)


def get_profile(user_id):

    result = (
        supabase
        .table("users")
        .select(
            "id,name,email,role"
        )
        .eq("id", user_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result.data[0]


def update_profile(user_id, data):

    result = (
        supabase
        .table("users")
        .update(data)
        .eq("id", user_id)
        .execute()
    )

    return result.data[0]


def change_password(
    user_id,
    old_password,
    new_password
):

    result = (
        supabase
        .table("users")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user = result.data[0]

    if not verify_password(
        old_password,
        user["password"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect"
        )

    hashed_password = hash_password(
        new_password
    )

    (
        supabase
        .table("users")
        .update({
            "password": hashed_password
        })
        .eq("id", user_id)
        .execute()
    )

    return {
        "message": "Password updated successfully"
    }