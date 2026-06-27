from app.core.supabase import supabase
from fastapi import HTTPException
from app.services.notification_service import create_notification

def get_all_products(
    page=1,
    limit=10,
    search=None,
    category=None,
    min_price=None,
    max_price=None,
    in_stock=None,
    sort_by=None,
):
    query = (
        supabase
        .table("products")
        .select("*")
    )

    if search:
        query = query.ilike(
            "name",
            f"%{search}%"
        )

    if category:
        query = query.eq(
            "category",
            category
        )

    if min_price is not None:
        query = query.gte(
            "price",
            min_price
        )

    if max_price is not None:
        query = query.lte(
            "price",
            max_price
        )

    if in_stock:
        query = query.gt(
            "stock",
            0
        )

    if sort_by == "price_asc":
        query = query.order("price")

    elif sort_by == "price_desc":
        query = query.order(
            "price",
            desc=True
        )

    elif sort_by == "newest":
        query = query.order(
            "created_at",
            desc=True
        )

    start = (page - 1) * limit
    end = start + limit - 1

    result = (
        query
        .range(start, end)
        .execute()
    )

    return result.data
def get_related_products(product_id: str):

    product = (
        supabase
        .table("products")
        .select("category")
        .eq("id", product_id)
        .single()
        .execute()
    )

    if not product.data:
        return []

    category = product.data["category"]

    related = (
        supabase
        .table("products")
        .select("*")
        .eq("category", category)
        .neq("id", product_id)
        .limit(4)
        .execute()
    )

    return related.data

def get_product(product_id):

    result = (
        supabase
        .table("products")
        .select("*")
        .eq("id", product_id)
        .execute()
    )

    if result.data:
        return result.data[0]

    return {
        "message": "Product not found"
    }

def create_product(data):
    try:
        print("DATA RECEIVED:", data)

        result = (
            supabase
            .table("products")
            .insert(data)
            .execute()
        )

        print("SUPABASE RESPONSE:", result.data)

        return result.data

    except Exception as e:
        print("CREATE PRODUCT ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def update_product(
    product_id: str,
    product_data: dict
):

    response = (
        supabase
        .table("products")
        .update(product_data)
        .eq("id", product_id)
        .execute()
    )

    if (
        "stock" in product_data and
        product_data["stock"] <= 5
    ):

        create_notification(

            "Low Stock",

            f"{product_data.get('name', 'Product')} has only {product_data['stock']} items remaining.",

            "low_stock"

        )

    return response.data
    

def delete_product(product_id: str):
    response = (
        supabase
        .table("products")
        .delete()
        .eq("id", product_id)
        .execute()
    )

    return response.data
def search_products(keyword):

    result = (
        supabase
        .table("products")
        .select("*")
        .ilike("name", f"%{keyword}%")
        .execute()
    )

    return result.data


def filter_products(category):

    result = (
        supabase
        .table("products")
        .select("*")
        .eq("category", category)
        .execute()
    )

    return result.data