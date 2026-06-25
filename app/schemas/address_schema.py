from pydantic import BaseModel
from typing import Optional


class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line: str
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None


class AddressUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None