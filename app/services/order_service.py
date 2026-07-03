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
        "payment_status": "Pending",
        "total_amount": final_total,
        "status": "Pending"
    }).execute()
    )

    order_id = order.data[0]["id"]

    # Save Shipping Address

    supabase.table("shipping_addresses").insert({
        "order_id": order_id,
        "full_name": data["full_name"],
        "email": data["email"],
        "phone": data["phone"],
        "city": data["city"],
        "address": data["address"],
        "postal_code": data["postal_code"],
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
        .select(
            """
            id,
            total_amount,
            status,
            payment_status,
            payment_method,
            created_at
            """
        )
        .eq(
            "user_id",
            user_id
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()

    )

    return result.data



def get_order(order_id):

    order = (
        supabase
        .table("orders")
        .select("*")
        .eq("id", order_id)
        .single()
        .execute()
    )

    if not order.data:
        return {"message": "Order not found"}

    shipping = (
        supabase
        .table("shipping_addresses")
        .select("*")
        .eq("order_id", order_id)
        .single()
        .execute()
    )

    items = (
        supabase
        .table("order_items")
        .select("""
            id,
            quantity,
            price,
            products(*)
        """)
        .eq("order_id", order_id)
        .execute()
    )

    return {
        "order": order.data,
        "shipping": shipping.data,
        "items": items.data
    }


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

    orders = (
        supabase
        .table("orders")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    result = []

    for order in orders.data:

        # Shipping
        shipping = (
            supabase
            .table("shipping_addresses")
            .select("*")
            .eq("order_id", order["id"])
            .execute()
        )

        # Order Items
        items = (
            supabase
            .table("order_items")
            .select("""
                id,
                quantity,
                price,
                products(
                    id,
                    name,
                    image_url,
                    price
                )
            """)
            .eq("order_id", order["id"])
            .execute()
        )
        result.append({
            **order,
            "shipping": shipping.data[0] if shipping.data else None,
            "items": items.data or []
        })

    return result



def track_order(order_id):

    result = (
        supabase
        .table("orders")
        .select("""
            id,
            status,
            tracking_number,
            created_at,
            payment_status,
            payment_method
        """)
        .eq("id", order_id)
        .single()
        .execute()
    )

    if not result.data:
        return {
            "message": "Order not found"
        }

    return result.data

def get_order_details(order_id, user_id):

    order = (
        supabase
        .table("orders")
        .select("*")
        .eq("id", order_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if not order.data:
        return None

    items = (
        supabase
        .table("order_items")
        .select("""
            *,
            products(*)
        """)
        .eq("order_id", order_id)
        .execute()
    )

    shipping = (
        supabase
        .table("shipping_addresses")
        .select("*")
        .eq("order_id", order_id)
        .single()
        .execute()
    )

    return {
        "order": order.data,
        "items": items.data,
        "shipping": shipping.data
    }
def cancel_order(order_id: str, user_id: str):

    # Get order
    order = (
        supabase
        .table("orders")
        .select("*")
        .eq("id", order_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if not order.data:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Check status
    if order.data["status"] != "Pending":

        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled."
        )

    # Get all order items
    items = (
        supabase
        .table("order_items")
        .select("*")
        .eq("order_id", order_id)
        .execute()
    )

    # Restore stock
    for item in items.data:

        product = (
            supabase
            .table("products")
            .select("stock")
            .eq("id", item["product_id"])
            .single()
            .execute()
        )

        new_stock = (
            product.data["stock"]
            + item["quantity"]
        )

        (
            supabase
            .table("products")
            .update({
                "stock": new_stock
            })
            .eq("id", item["product_id"])
            .execute()
        )

    # Cancel order
    (
        supabase
        .table("orders")
        .update({
            "status": "Cancelled"
        })
        .eq("id", order_id)
        .execute()
    )

    create_notification(
        "Order Cancelled",
        f"Your order #{order_id} has been cancelled.",
        "order"
    )

    return {
        "message": "Order cancelled successfully."
    }