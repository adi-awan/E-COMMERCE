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
        .select(
            """
            id,
            quantity,
            products(*)
            """
        )
        .eq(
            "cart_id",
            cart["id"]
        )
        .execute()
    )


    if not cart_items.data:

        return {
            "message": "Cart is empty"
        }



    # stock checking

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
            *
            item["products"]["price"]
        )

    discount = 0
    final_total = subtotal

    order = (

        supabase
        .table("orders")
        .insert({

            "user_id": user_id,

            "total_amount": final_total,

            "status": "Pending",

            "payment_status": "Pending"

        })
        .execute()

    )


    order_id = order.data[0]["id"]




    for item in cart_items.data:

        product = item["products"]

        supabase.table(
            "order_items"
        ).insert({
            "order_id": order_id,
            "product_id": product["id"],
            "quantity": item["quantity"],
            "price": product["price"]
        }).execute()

        # decrease stock
        supabase.table(
            "products"
        ).update({
            "stock": product["stock"] - item["quantity"]
        }).eq(
            "id",
            product["id"]
        ).execute()


    # Create ONE notification after the entire order is completed
    create_notification(
        "New Order",
        f"Order #{order_id} has been placed.",
        "new_order"
    )

    # clear cart

    supabase.table(
        "cart_items"
    ).delete().eq(
        "cart_id",
        cart["id"]
    ).execute()


    # get user email

    user_result = (

        supabase
        .table("users")
        .select("email,name")
        .eq(
            "id",
            user_id
        )
        .execute()

    )


    if user_result.data:

        user = user_result.data[0]


        # asyncio.run(

        #     send_email(

        #         user["email"],

        #         "Order Confirmed",

        #         f"""
        #         <h2>Your order is confirmed</h2>

        #         <p>
        #         Order ID: {order_id}
        #         </p>

        #         <p>
        #         Total: {final_total}
        #         </p>
        #         """

        #     )

        # )



    return {

        "message":
        "Order placed successfully",

        "order_id":
        order_id,

        "subtotal":
        subtotal,

        "discount":
        discount,

        "final_total":
        final_total

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