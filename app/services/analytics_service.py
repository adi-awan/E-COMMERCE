from app.core.supabase import supabase


def revenue_summary():

    orders = (
        supabase
        .table("orders")
        .select("*")
        .execute()
    )

    total_revenue = 0

    for order in orders.data:
        total_revenue += order.get(
            "total_amount",
            0
        )

    return {
        "total_revenue": total_revenue,
        "total_orders": len(orders.data)
    }


def top_products():

    items = (
        supabase
        .table("order_items")
        .select(
            """
            quantity,
            products(
                id,
                name
            )
            """
        )
        .execute()
    )

    stats = {}

    for item in items.data:

        product = item["products"]

        name = product["name"]

        if name not in stats:
            stats[name] = 0

        stats[name] += item["quantity"]

    result = []

    for name, sold in stats.items():

        result.append({
            "product": name,
            "sold": sold
        })

    result.sort(
        key=lambda x: x["sold"],
        reverse=True
    )

    return result[:10]