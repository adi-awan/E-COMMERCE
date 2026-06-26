from app.core.supabase import supabase


def get_categories():

    result = (
        supabase
        .table("categories")
        .select("*")
        .order("name")
        .execute()
    )

    return result.data


def create_category(data):

    result = (
        supabase
        .table("categories")
        .insert(data)
        .execute()
    )

    return result.data


def update_category(category_id, data):

    result = (
        supabase
        .table("categories")
        .update(data)
        .eq("id", category_id)
        .execute()
    )

    return result.data


def delete_category(category_id):

    result = (
        supabase
        .table("categories")
        .delete()
        .eq("id", category_id)
        .execute()
    )

    return result.data