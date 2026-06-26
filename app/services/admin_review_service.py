from app.core.supabase import supabase


def get_all_reviews():

    result = (
        supabase
        .table("review_details")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return result.data


def get_review_stats():

    reviews = (
        supabase
        .table("reviews")
        .select("*")
        .execute()
    )

    total = len(reviews.data)

    average = 0

    if total:

        average = round(
            sum(r["rating"] for r in reviews.data) / total,
            2
        )

    return {
        "total_reviews": total,
        "average_rating": average
    }


def delete_review(review_id):

    result = (
        supabase
        .table("reviews")
        .delete()
        .eq("id", review_id)
        .execute()
    )

    return result.data