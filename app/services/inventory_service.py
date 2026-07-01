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
        .select("stock,name")
        .eq("id", product_id)
        .single()
        .execute()
    )

    if not product.data:
        return {
            "message": "Product not found"
        }

    current_stock = product.data["stock"]
    product_name = product.data["name"]

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

    try:
        create_notification(
            "Inventory Updated",
            f"{product_name} inventory updated. Current stock: {new_stock}",
            "inventory"
        )
    except Exception as e:
        print(e)

    return result.data