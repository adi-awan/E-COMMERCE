from app.core.supabase import supabase


def get_or_create_cart(user_id):

    result = (
        supabase
        .table("carts")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )


    if result.data:
        return result.data[0]


    new_cart = (
        supabase
        .table("carts")
        .insert({
            "user_id": user_id
        })
        .execute()
    )


    return new_cart.data[0]



def get_cart(user_id):

    cart = get_or_create_cart(user_id)


    items = (
        supabase
        .table("cart_items")
        .select(
            """
            id,
            quantity,
            products(*)
            """
        )
        .eq(
            "cart_id",
            cart["id"]
        )
        .execute()
    )


    return {
        "cart_id": cart["id"],
        "items": items.data
    }



def add_to_cart(user_id, data):

    cart = get_or_create_cart(user_id)


    existing = (
        supabase
        .table("cart_items")
        .select("*")
        .eq(
            "cart_id",
            cart["id"]
        )
        .eq(
            "product_id",
            data["product_id"]
        )
        .execute()
    )


    if existing.data:

        item = existing.data[0]


        updated = (
            supabase
            .table("cart_items")
            .update({
                "quantity":
                item["quantity"] + data["quantity"]
            })
            .eq(
                "id",
                item["id"]
            )
            .execute()
        )


        return updated.data


    result = (
        supabase
        .table("cart_items")
        .insert({
            "cart_id": cart["id"],
            "product_id": data["product_id"],
            "quantity": data["quantity"]
        })
        .execute()
    )


    return result.data



def update_cart_item(user_id, item_id, quantity):

    result = (
        supabase
        .table("cart_items")
        .update({
            "quantity": quantity
        })
        .eq(
            "id",
            item_id
        )
        .eq(
            "cart_id",
            user_id
        )
        .execute()
    )

    return result.data


def remove_cart_item(user_id, item_id):

    result = (
        supabase
        .table("cart_items")
        .delete()
        .eq("id", item_id)
        .eq("cart_id", user_id)
        .execute()
    )


    return result.data