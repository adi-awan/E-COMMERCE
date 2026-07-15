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
        total_revenue += order.get(
            "total_amount",
            0
        )

    return {
        "total_users": users.count,
        "total_products": products.count,
        "total_orders": len(orders.data),
        "total_revenue": total_revenue
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
        .order("stock")
        .execute()
    )

    return result.data


def get_all_orders():

    result = (
        supabase
        .table("orders")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return result.data


def get_order(order_id):

    result = (
        supabase
        .table("orders")
        .select("*")
        .eq("id", order_id)
        .single()
        .execute()
    )

    return result.data


def update_order_status(
    order_id,
    status
):

    result = (
        supabase
        .table("orders")
        .update({
            "status": status
        })
        .eq(
            "id",
            order_id
        )
        .execute()
    )

    return result.data


def delete_order(order_id):

    result = (
        supabase
        .table("orders")
        .delete()
        .eq(
            "id",
            order_id
        )
        .execute()
    )

    return result.data
def get_all_users():

    result = (
        supabase
        .table("users")
        .select("id,name,email,role,email_verified,created_at")
        .order("created_at", desc=True)
        .execute()
    )

    return result.data


def get_user(user_id):

    result = (
        supabase
        .table("users")
        .select("id,name,email,role,email_verified,created_at")
        .eq("id", user_id)
        .single()
        .execute()
    )

    return result.data


def update_user_role(user_id, role):

    result = (
        supabase
        .table("users")
        .update({
            "role": role
        })
        .eq("id", user_id)
        .execute()
    )

    return result.data


def delete_user(user_id):

    result = (
        supabase
        .table("users")
        .delete()
        .eq("id", user_id)
        .execute()
    )

    return result.data

def get_all_reviews():

    result = (
        supabase
        .table("reviews")
        .select(
            """
            *,
            users(name),
            products(name)
            """
        )
        .order("created_at", desc=True)
        .execute()
    )

    reviews = []

    for review in result.data:

        reviews.append({

            "id": review["id"],

            "rating": review["rating"],

            "comment": review["comment"],

            "created_at": review["created_at"],

            "user_name": (
                review["users"]["name"]
                if review.get("users")
                else "Unknown User"
            ),

            "product_name": (
                review["products"]["name"]
                if review.get("products")
                else "Unknown Product"
            )

        })

    return reviews


def review_statistics():

    result = (
        supabase
        .table("reviews")
        .select("*")
        .execute()
    )

    total = len(result.data)

    if total == 0:

        return {

            "total_reviews": 0,

            "average_rating": 0

        }

    avg = sum(

        review["rating"]

        for review in result.data

    ) / total

    return {

        "total_reviews": total,

        "average_rating": round(avg, 2)

    }


def admin_delete_review(review_id):

    (
        supabase
        .table("reviews")
        .delete()
        .eq("id", review_id)
        .execute()
    )

    return {

        "message": "Review deleted"

    }