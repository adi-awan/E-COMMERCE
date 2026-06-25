from app.core.supabase import supabase


def upload_image(file):

    file_bytes = file.file.read()

    path = f"products/{file.filename}"

    supabase.storage.from_("product-images").upload(
        path,
        file_bytes,
        {"content-type": file.content_type}
    )

    url = supabase.storage.from_(
        "product-images"
    ).get_public_url(path)

    return {
        "image_url": url
    }