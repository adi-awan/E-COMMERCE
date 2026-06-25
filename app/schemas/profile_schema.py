from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str