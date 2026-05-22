from typing import List, Optional, Tuple

import requests
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from config import settings
from database.models import Post
from database.schema import PostUpdate

UPLOAD_URL = "https://upload.imagekit.io/api/v1/files/upload"
DELETE_URL = "https://api.imagekit.io/v1/files"


def to_dict(post: Post) -> dict:
    return {
        "id": post.id,
        "caption": post.caption,
        "image_url": post.image_url,
        "image_file_id": post.image_file_id,
        "created_at": post.created_at,
    }


def ensure_imagekit():
    if not settings.imagekit_private_key or not settings.imagekit_url:
        raise HTTPException(500, "ImageKit not configured")


def upload_image(file: UploadFile) -> Tuple[str, Optional[str]]:
    ensure_imagekit()
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only images allowed")

    data = file.file.read()
    if not data:
        raise HTTPException(400, "Empty file")

    files = {
        "file": (file.filename or "image", data, file.content_type or "application/octet-stream")
    }

    resp = requests.post(UPLOAD_URL, auth=(settings.imagekit_private_key, ""), files=files, timeout=30)
    if resp.status_code >= 400:
        raise HTTPException(502, "ImageKit upload failed")

    j = resp.json()
    return j.get("url"), j.get("fileId")


def create_post(db: Session, caption: str, image: UploadFile) -> dict:
    url, file_id = upload_image(image)
    post = Post(caption=caption or "", image_url=url, image_file_id=file_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return to_dict(post)


def list_posts(db: Session) -> List[dict]:
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return [to_dict(p) for p in posts]


def get_post(db: Session, post_id: int) -> dict:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    return to_dict(post)


def update_post(db: Session, post_id: int, data: PostUpdate) -> dict:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if data.caption is not None:
        post.caption = data.caption
    db.commit()
    db.refresh(post)
    return to_dict(post)


def delete_post(db: Session, post_id: int) -> dict:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.image_file_id:
        try:
            requests.delete(f"{DELETE_URL}/{post.image_file_id}", auth=(settings.imagekit_private_key, ""), timeout=30)
        except requests.RequestException:
            pass
    db.delete(post)
    db.commit()
    return {"message": "deleted", "post_id": post_id}
