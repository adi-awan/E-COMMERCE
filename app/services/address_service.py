from app.core.supabase import supabase


def get_addresses(user_id):

    result = (
        supabase
        .table("addresses")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return result.data


def add_address(user_id, data):

    data["user_id"] = user_id

    result = (
        supabase
        .table("addresses")
        .insert(data)
        .execute()
    )

    return result.data


def update_address(address_id, data):

    result = (
        supabase
        .table("addresses")
        .update(data)
        .eq("id", address_id)
        .execute()
    )

    return result.data


def delete_address(address_id):

    (
        supabase
        .table("addresses")
        .delete()
        .eq("id", address_id)
        .execute()
    )

    return {
        "message": "Address deleted"
    }