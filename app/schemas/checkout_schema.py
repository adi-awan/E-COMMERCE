from pydantic import BaseModel


class CheckoutRequest(BaseModel):

    full_name: str
    email: str
    phone: str
    city: str
    address: str
    postal_code: str
    payment_method: str