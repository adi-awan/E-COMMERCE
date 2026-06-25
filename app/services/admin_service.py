from app.core.supabase import supabase


def dashboard_stats():

    users = (
        supabase
        .table("users")
        .select("*", count="exact")
        .execute()
    )

    products = (
        supabase
        .table("products")
        .select("*", count="exact")
        .execute()
    )

    orders = (
        supabase
        .table("orders")
        .select("*")
        .execute()
    )

    total_revenue = 0

    for order in orders.data:

        total_revenue += (
            order.get(
                "total_amount",
                0
            )
        )

    return {

        "total_users":
        users.count,

        "total_products":
        products.count,

        "total_orders":
        len(orders.data),

        "total_revenue":
        total_revenue

    }


def recent_orders():

    result = (

        supabase
        .table("orders")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .limit(10)
        .execute()

    )

    return result.data


def low_stock_products():

    result = (

        supabase
        .table("products")
        .select("*")
        .lte(
            "stock",
            5
        )
        .order(
            "stock"
        )
        .execute()

    )

    return result.data