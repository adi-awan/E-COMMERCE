from app.core.supabase import supabase


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

    return result.data


def update_review(review_id, data):

    result = (
        supabase
        .table("reviews")
        .update(data)
        .eq("id", review_id)
        .execute()
    )

    return result.data


def delete_review(review_id):

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