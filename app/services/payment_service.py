import stripe

from app.core.config import STRIPE_SECRET_KEY
from app.core.supabase import supabase

stripe.api_key = STRIPE_SECRET_KEY


def create_payment(order_id):

    order = (
        supabase
        .table("orders")
        .select("*")
        .eq("id", order_id)
        .execute()
    )

    if not order.data:
        return {
            "message": "Order not found"
        }

    order = order.data[0]

    amount = int(
        order["total_amount"] * 100
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Order {order_id}"
                    },
                    "unit_amount": amount
                },
                "quantity": 1
            }
        ],
        mode="payment",
        success_url="http://localhost:3000/payment-success",
        cancel_url="http://localhost:3000/payment-cancel"
    )

    return {
        "checkout_url": session.url
    }


def verify_payment(order_id):

    (
        supabase
        .table("orders")
        .update({
            "payment_status": "Paid"
        })
        .eq("id", order_id)
        .execute()
    )

    return {
        "message": "Payment verified"
    }