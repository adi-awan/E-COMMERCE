from app.core.supabase import supabase


def get_or_create_wishlist(user_id):

    result = (
        supabase
        .table("wishlists")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if result.data:
        return result.data[0]

    new_wishlist = (
        supabase
        .table("wishlists")
        .insert({
            "user_id": user_id
        })
        .execute()
    )

    return new_wishlist.data[0]


def get_wishlist(user_id):

    wishlist = get_or_create_wishlist(user_id)

    items = (
        supabase
        .table("wishlist_items")
        .select(
            """
            id,
            products(*)
            """
        )
        .eq(
            "wishlist_id",
            wishlist["id"]
        )
        .execute()
    )

    return {
        "wishlist_id": wishlist["id"],
        "items": items.data
    }


def add_to_wishlist(user_id, product_id):

    wishlist = get_or_create_wishlist(user_id)

    existing = (
        supabase
        .table("wishlist_items")
        .select("*")
        .eq("wishlist_id", wishlist["id"])
        .eq("product_id", product_id)
        .execute()
    )

    if existing.data:
        return {
            "message": "Product already in wishlist"
        }

    result = (
        supabase
        .table("wishlist_items")
        .insert({
            "wishlist_id": wishlist["id"],
            "product_id": product_id
        })
        .execute()
    )

    return result.data


def remove_from_wishlist(user_id, item_id):

    wishlist = get_or_create_wishlist(user_id)

    result = (
        supabase
        .table("wishlist_items")
        .delete()
        .eq("id", item_id)
        .eq("wishlist_id", wishlist["id"])
        .execute()
    )

    if not result.data:
        return {
            "message": "Wishlist item not found."
        }

    return {
        "message": "Item removed successfully."
    }