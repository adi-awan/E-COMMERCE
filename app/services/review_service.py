from app.core.supabase import supabase
from app.services.notification_service import create_notification

def get_reviews(product_id):

    result = (
        supabase
        .table("reviews")
        .select("*")
        .eq("product_id", product_id)
        .execute()
    )

    return result.data


def add_review(user_id, data):

    review = {
        "user_id": user_id,
        "product_id": data["product_id"],
        "rating": data["rating"],
        "comment": data["comment"]
    }

    result = (
        supabase
        .table("reviews")
        .insert(review)
        .execute()
    )

    product = (
        supabase
        .table("products")
        .select("name")
        .eq("id", data["product_id"])
        .single()
        .execute()
    )

    create_notification(

        "New Review",

        f"{product.data['name']} received a {data['rating']}-star review.",

        "new_review"

    )

    return result.data

def update_review(review_id, user_id, data):

    result = (
        supabase
        .table("reviews")
        .update(data)
        .eq("id", review_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not result.data:
        return {"message": "Review not found"}

    return result.data


def delete_review(review_id, user_id):

    result = (
        supabase
        .table("reviews")
        .delete()
        .eq("id", review_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not result.data:
        return {"message": "Review not found"}

    return {
        "message": "Review deleted"
    }