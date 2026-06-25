from fastapi import APIRouter,Query, Depends, UploadFile, File
from typing import Optional
from typing import Annotated
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
)

from app.services.product_service import (
    get_all_products,
    get_product,
    create_product,
    update_product,
    delete_product,
    search_products,
    filter_products
)
from app.core.dependencies import get_current_user
from app.core.roles import admin_required
from app.services.upload_service import upload_image

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# =========================
# Public Routes
# =========================

@router.get("/")
def get_products(

    page: int = 1,

    limit: int = 10,

    category: Optional[str] = None,

    min_price: Optional[float] = None,

    max_price: Optional[float] = None,

    sort_by: Optional[str] = None

):

    return get_all_products(
        page,
        limit,
        category,
        min_price,
        max_price,
        sort_by
    )

@router.get("/search/")
def search(
    keyword: str = Query(...)
):
    return search_products(keyword)

@router.get("/filter/")
def filter_by_category(
    category: str = Query(...)
):
    return filter_products(category)

@router.get("/{product_id}")
def get_single_product(product_id: str):
    return get_product(product_id)


# =========================
# Admin Routes
# =========================

@router.post("/")
def add_product(
    product: ProductCreate,
    user=Depends(admin_required)
):
    return create_product(
        product.model_dump()
    )


@router.put("/{product_id}")
def edit_product(
    product_id: str,
    product: ProductUpdate,
    user=Depends(admin_required)
):
    return update_product(
        product_id,
        product.model_dump()
    )


@router.delete("/{product_id}")
def remove_product(
    product_id: str,
    user=Depends(admin_required)
):
    return delete_product(
        product_id
    )
@router.post("/upload-image")
def upload_product_image(
    file: UploadFile = File(...),
    user=Depends(admin_required)
):
    return upload_image(file)