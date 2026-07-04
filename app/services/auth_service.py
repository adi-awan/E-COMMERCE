from fastapi import HTTPException
import secrets

from datetime import datetime, timedelta
from app.core.supabase import supabase

# from app.services.email_service import send_email
import secrets
from datetime import datetime, timedelta
from app.core.security import (
    hash_password,
    verify_password,
    create_token
)
import asyncio
from app.services.email_service import send_email



def register_user(data):


    existing = (
        supabase
        .table("users")
        .select("id")
        .eq(
            "email",
            data["email"]
        )
        .execute()
    )


    if existing.data:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    password = hash_password(
        data["password"]
    )


    verification_token = secrets.token_urlsafe(32)

    verification_expiry = (
        datetime.utcnow() +
        timedelta(minutes=15)
    ).isoformat()

    user = {

        "name": data["name"],

        "email": data["email"],

        "password": password,

        "email_verified": False,

        "verification_token": verification_token,

        "verification_token_expiry": verification_expiry,

    }


    response = (

        supabase
        .table("users")
        .insert(user)
        .execute()

    )
    verification_link = f"http://localhost:8000/auth/verify-email?token={verification_token}"

    asyncio.run(
        send_email(
            data["email"],
            "Verify Your Email",
            f"""
            <h2>Welcome {data['name']}</h2>
            <p>Please verify your email:</p>
            <a href="{verification_link}">Click here to verify</a>
            """
        )
    )




    return response.data

def verify_email(token: str):

    result = (
        supabase
        .table("users")
        .select("*")
        .eq("verification_token", token)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )

    user = result.data[0]

    expiry = datetime.fromisoformat(
        user["verification_token_expiry"]
    )

    if expiry < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Verification link has expired"
        )

    (
        supabase
        .table("users")
        .update({
            "email_verified": True,
            "verification_token": None,
            "verification_token_expiry": None,
        })
        .eq("id", user["id"])
        .execute()
    )

    return {
        "message": "Email verified successfully"
    }



def login_user(email, password):


    response = (

        supabase
        .table("users")
        .select("*")
        .eq(
            "email",
            email
        )
        .execute()

    )


    if not response.data:

        return None



    user = response.data[0]



    if not verify_password(
        password,
        user["password"]
    ):

        return None



    token = create_token(

        {
            "id": user["id"],

            "role": user["role"],

            "name": user["name"]

        }

    )


    return {

        "access_token": token,

        "token_type": "bearer"

    }
def forgot_password(email):


    user = (
        supabase
        .table("users")
        .select("*")
        .eq(
            "email",
            email
        )
        .execute()
    )


    if not user.data:
        return {
            "message":
            "Email not found"
        }


    token = secrets.token_urlsafe(32)


    (
        supabase
        .table("users")
        .update({

            "reset_token": token,

            "reset_token_expiry":
            (
                datetime.utcnow()
                +
                timedelta(minutes=15)
            ).isoformat()

        })
        .eq(
            "email",
            email
        )
        .execute()
    )


    # asyncio.run(

    #     send_email(

    #         email,

    #         "Password Reset",

    #         f"""
    #         <h2>Password Reset</h2>

    #         <p>
    #         Your reset token:
    #         </p>

    #         <b>{token}</b>
    #         """

    #     )

    # )


    return {
        "message":
        "Reset email sent"
    }




def reset_password(token,new_password):


    result = (

        supabase
        .table("users")
        .select("*")
        .eq(
            "reset_token",
            token
        )
        .execute()

    )


    if not result.data:

        return {
            "message":
            "Invalid token"
        }



    user = result.data[0]


    password = hash_password(
        new_password
    )


    (
        supabase
        .table("users")
        .update({

            "password": password,

            "reset_token": None

        })
        .eq(
            "id",
            user["id"]
        )
        .execute()
    )


    return {
        "message":
        "Password updated"
    }