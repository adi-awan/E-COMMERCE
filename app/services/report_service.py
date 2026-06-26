app/services/report_service.pyfrom app.core.supabase import supabase


def sales_report():

    orders = (
        supabase
        .table("orders")
        .select("*")
        .execute()
    )


    total_sales = 0
    total_orders = len(
        orders.data
    )


    for order in orders.data:

        total_sales += order.get(
            "total_amount",
            0
        )


    return {

        "total_orders":
        total_orders,

        "total_sales":
        total_sales,

        "orders":
        orders.data

    }