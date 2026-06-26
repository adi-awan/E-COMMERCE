from app.core.supabase import supabase


def get_all_shipments():

    result = (
        supabase
        .table("shipping")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return result.data


def get_shipping(order_id):

    result = (
        supabase
        .table("shipping")
        .select("*")
        .eq("order_id", order_id)
        .single()
        .execute()
    )

    return result.data


def create_shipping(data):

    result = (
        supabase
        .table("shipping")
        .insert(data)
        .execute()
    )

    return result.data


def update_shipping(shipping_id, data):

    result = (
        supabase
        .table("shipping")
        .update(data)
        .eq("id", shipping_id)
        .execute()
    )

    return result.data


def delete_shipping(shipping_id):

    result = (
        supabase
        .table("shipping")
        .delete()
        .eq("id", shipping_id)
        .execute()
    )

    return result.data