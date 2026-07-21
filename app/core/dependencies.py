from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.core.supabase import supabase

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # Always pull the live user record instead of trusting the token's
    # cached claims — role (or even the account itself) may have
    # changed since this token was issued.
    result = (
        supabase
        .table("users")
        .select("id, name, email, role")
        .eq("id", payload["id"])
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=401,
            detail="User no longer exists"
        )

    return result.data[0]