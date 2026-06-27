from fastapi import APIRouter, UploadFile, File, Depends

from app.core.roles import admin_required

# 👇 Import the function
from app.services.upload_service import upload_image

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/upload-image")
def upload_product_image(
    file: UploadFile = File(...),
    user=Depends(admin_required)
):
    return upload_image(file)