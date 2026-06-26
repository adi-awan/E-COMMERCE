from app.core.supabase import supabase
from app.services.notification_service import create_notification

def get_inventory():

    result = (
        supabase
        .table("products")
        .select("*")
        .order("name")
        .execute()
    )

    return result.data


def low_stock_products():

    result = (
        supabase
        .table("products")
        .select("*")
        .lte("stock", 5)
        .order("stock")
        .execute()
    )

    return result.data


def update_stock(product_id, quantity):

    product = (
        supabase
        .table("products")
        .select("stock")
        .eq("id", product_id)
        .single()
        .execute()
    )

    current_stock = product.data["stock"]

    new_stock = current_stock + quantity

    if new_stock < 0:
        new_stock = 0

    result = (
        supabase
        .table("products")
        .update({
            "stock": new_stock
        })
        .eq("id", product_id)
        .execute()
    )
    create_notification(

    "Inventory Updated",

    f"{product_name} inventory updated.",

    "inventory"

)
    return result.data