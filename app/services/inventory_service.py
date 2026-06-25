from app.core.supabase import supabase


def low_stock_products():

    result = (
        supabase
        .table("products")
        .select("*")
        .lte(
            "stock",
            5
        )
        .execute()
    )

    return result.data