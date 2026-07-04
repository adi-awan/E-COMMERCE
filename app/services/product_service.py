from app.core.supabase import supabase
from fastapi import HTTPException
from app.services.notification_service import create_notification

def add_rating_info(product):

    reviews = (
        supabase
        .table("reviews")
        .select("rating")
        .eq("product_id", product["id"])
        .execute()
    ).data

    if reviews:
        average = sum(
            review["rating"] for review in reviews
        ) / len(reviews)

        product["rating"] = round(average, 1)
        product["review_count"] = len(reviews)

    else:
        product["rating"] = 0
        product["review_count"] = 0

    return product

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
        query = query.or_(

            f"name.ilike.%{search}%," +
            f"description.ilike.%{search}%," +
            f"category.ilike.%{search}%"

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

    products = result.data

    for product in products:
        add_rating_info(product)

    return products

def get_related_products(product_id: str):

    product = (
        supabase
        .table("products")
        .select("category")
        .eq("id", product_id)
        .single()
        .execute()
    )

    products = related.data

    for product in products:
        add_rating_info(product)

    return products

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

        product = result.data[0]

        add_rating_info(product)

        return product

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
def get_product_suggestions(keyword: str):

    result = (
        supabase
        .table("products")
        .select("id, name, image_url, price")
        .or_(
            f"name.ilike.%{keyword}%,"
            f"description.ilike.%{keyword}%,"
            f"category.ilike.%{keyword}%"
        )
        .limit(8)
        .execute()
    )

    return result.data
