from app.core.supabase import supabase


def get_coupon(code):

    result = (
        supabase
        .table("coupons")
        .select("*")
        .eq("code", code)
        .eq("active", True)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


def create_coupon(data):

    result = (
        supabase
        .table("coupons")
        .insert(data)
        .execute()
    )

    return result.data


def get_all_coupons():

    result = (
        supabase
        .table("coupons")
        .select("*")
        .execute()
    )

    return result.data