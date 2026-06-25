from fastapi import FastAPI

from app.routes.products import router as product_router
from app.routes.auth import router as auth_router
from app.routes.cart import router as cart_router
from app.routes.orders import router as order_router
from app.routes.upload import router as upload_router
from app.routes.wishlist import router as wishlist_router
from app.routes.profile import router as profile_router
from app.routes.reviews import router as review_router
from app.routes.addresses import router as address_router
from app.routes.coupons import router as coupon_router
from app.routes.admin import router as admin_router
from app.routes.analytics import router as analytics_router
from app.routes.inventory import router as inventory_router
from app.routes.admin import router as admin_router



app = FastAPI()


app.include_router(product_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(upload_router)
app.include_router(wishlist_router)
app.include_router(profile_router)
app.include_router(review_router)
app.include_router(address_router)
app.include_router(coupon_router)
app.include_router(admin_router)
app.include_router(analytics_router)
app.include_router(inventory_router)
app.include_router(admin_router)


@app.get("/")
def home():
    return {
        "message": "API running"
    }