from fastapi import HTTPException
from app.core.supabase import supabase


def upload_image(file):

    try:

        file_bytes = file.file.read()

        path = f"products/{file.filename}"

        response = (
            supabase
            .storage
            .from_("product-images")
            .upload(
                path,
                file_bytes,
                {
                    "content-type": file.content_type,
                    "upsert": "true"
                }
            )
        )

        url = (
            supabase
            .storage
            .from_("product-images")
            .get_public_url(path)
        )

        return {
            "image_url": url
        }

    except Exception as e:

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )