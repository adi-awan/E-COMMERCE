from fastapi import UploadFile, HTTPException
from app.core.supabase import supabase
import uuid


def upload_image(file: UploadFile):

    try:

        extension = file.filename.split(".")[-1]

        filename = f"{uuid.uuid4()}.{extension}"

        path = f"products/{filename}"

        file_bytes = file.file.read()

        supabase.storage.from_("product-images").upload(
            path,
            file_bytes,
            {
                "content-type": file.content_type,
                "upsert": "true"
            }
        )

        image_url = (
            supabase
            .storage
            .from_("product-images")
            .get_public_url(path)
        )

        return {
            "image_url": image_url
        }

    except Exception as e:

        print("UPLOAD ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )