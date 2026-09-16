from typing import Final

from fastapi import UploadFile

from app.core.supabase import supabase


MAX_IMAGE_SIZE: Final = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES: Final = {"image/jpeg", "image/png", "image/webp"}


async def upload_public_image(
    file: UploadFile,
    bucket: str,
    path: str,
) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("Formato de imagem inválido. Use JPEG, PNG ou WebP.")

    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise ValueError("A imagem deve ter no máximo 5 MB.")

    supabase.storage.from_(bucket).upload(
        path,
        content,
        {
            "content-type": file.content_type,
            "upsert": "true",
        },
    )

    return supabase.storage.from_(bucket).get_public_url(path)