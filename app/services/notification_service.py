from app.core.supabase import supabase


def get_notifications():

    result = (
        supabase
        .table("notifications")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return result.data


def create_notification(
    title,
    message,
    notification_type
):

    data = {
        "title": title,
        "message": message,
        "type": notification_type
    }

    result = (
        supabase
        .table("notifications")
        .insert(data)
        .execute()
    )

    return result.data


def mark_as_read(notification_id):

    result = (
        supabase
        .table("notifications")
        .update({
            "is_read": True
        })
        .eq(
            "id",
            notification_id
        )
        .execute()
    )

    return result.data


def mark_all_read():

    result = (
        supabase
        .table("notifications")
        .update({
            "is_read": True
        })
        .eq(
            "is_read",
            False
        )
        .execute()
    )

    return result.data


def delete_notification(notification_id):

    result = (
        supabase
        .table("notifications")
        .delete()
        .eq(
            "id",
            notification_id
        )
        .execute()
    )

    return result.data