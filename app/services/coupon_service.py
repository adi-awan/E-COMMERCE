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
def update_coupon(coupon_id, data):

    result = (
        supabase
        .table("coupons")
        .update(data)
        .eq("id", coupon_id)
        .execute()
    )

    return result.data


def delete_coupon(coupon_id):

    result = (
        supabase
        .table("coupons")
        .delete()
        .eq("id", coupon_id)
        .execute()
    )

    return result.data


def toggle_coupon(coupon_id):

    coupon = (
        supabase
        .table("coupons")
        .select("active")
        .eq("id", coupon_id)
        .single()
        .execute()
    )

    active = coupon.data["active"]

    result = (
        supabase
        .table("coupons")
        .update({
            "active": not active
        })
        .eq("id", coupon_id)
        .execute()
    )

    return result.data