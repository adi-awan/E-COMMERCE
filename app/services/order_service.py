from app.core.supabase import supabase
import uuid
from app.services.cart_service import get_or_create_cart
# from app.services.email_service import send_email
from app.services.notification_service import create_notification

# import asyncio



def checkout(user_id, data):

    cart = get_or_create_cart(user_id)

    cart_items = (
        supabase
        .table("cart_items")
        .select("""
            id,
            quantity,
            products(*)
        """)
        .eq("cart_id", cart["id"])
        .execute()
    )

    if not cart_items.data:
        return {
            "message": "Cart is empty"
        }

    # Check stock

    for item in cart_items.data:

        product = item["products"]

        if product["stock"] < item["quantity"]:
            return {
                "message":
                f"{product['name']} has insufficient stock"
            }

    subtotal = 0

    for item in cart_items.data:
        subtotal += (
            item["quantity"]
            * item["products"]["price"]
        )

    final_total = subtotal

    # Create Order

    order = (
        supabase.table("orders").insert({
            "user_id": user_id,
            "payment_method": data["payment_method"],
            "total_amount": final_total,
            "status": "Pending",
            "payment_status": "Pending"
        }).execute()
    )

    order_id = order.data[0]["id"]

    # Save Shipping Address

    supabase.table("shipping_addresses").insert({

        "order_id": order_id,

        "full_name": data.full_name,

        "email": data.email,

        "phone": data.phone,

        "city": data.city,

        "address": data.address,

        "postal_code": data.postal_code

    }).execute()

    # Save Order Items

    for item in cart_items.data:

        product = item["products"]

        supabase.table("order_items").insert({

            "order_id": order_id,

            "product_id": product["id"],

            "quantity": item["quantity"],

            "price": product["price"]

        }).execute()

        # Update Stock

        supabase.table("products").update({

            "stock":
            product["stock"] - item["quantity"]

        }).eq(
            "id",
            product["id"]
        ).execute()

    # Notification

    create_notification(
        "New Order",
        f"Order #{order_id} has been placed.",
        "new_order"
    )

    # Clear Cart

    supabase.table("cart_items").delete().eq(
        "cart_id",
        cart["id"]
    ).execute()

    return {

        "message": "Order placed successfully",

        "order_id": order_id,

        "subtotal": subtotal,

        "discount": 0,

        "final_total": final_total

    }




def get_orders(user_id):

    result = (
        supabase
        .table("orders")
        .select("*")
        .eq(
            "user_id",
            user_id
        )
        .execute()
    )

    return result.data





def get_order(order_id):

    result = (
        supabase
        .table("order_items")
        .select(
            """
            id,
            quantity,
            price,
            products(*)
            """
        )
        .eq(
            "order_id",
            order_id
        )
        .execute()
    )

    return result.data





def update_order_status(
    order_id,
    status
):

    update_data = {
        "status": status
    }


    if status == "Shipped":

        update_data[
            "tracking_number"
        ] = generate_tracking_number()


    result = (

        supabase
        .table("orders")
        .update(
            update_data
        )
        .eq(
            "id",
            order_id
        )
        .execute()

    )

    return result.data




def get_all_orders():

    result = (

        supabase
        .table("orders")
        .select("*")
        .execute()

    )

    return result.data
def generate_tracking_number():

    return str(
        uuid.uuid4()
    ).replace(
        "-",
        ""
    )[:12].upper()



def track_order(order_id):

    result = (
        supabase
        .table("orders")
        .select("*")
        .eq(
            "id",
            order_id
        )
        .execute()
    )

    if not result.data:

        return {
            "message":
            "Order not found"
        }

    return result.data[0]
