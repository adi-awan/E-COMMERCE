from fastapi import APIRouter
from fastapi import UploadFile, File
from app.core.roles import admin_required
from fastapi import Depends

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
def upload_image(
    file: UploadFile = File(...),
    user = Depends(admin_required)
):

    return {
        "filename": file.filename
    }