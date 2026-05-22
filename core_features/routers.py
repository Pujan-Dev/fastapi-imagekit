from typing import List

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from core_features.service import create_post, delete_post, get_post, list_posts, update_post
from database.database import get_db
from database.schema import PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=List[PostRead])
def read_posts(db: Session = Depends(get_db)):
    return list_posts(db)


@router.post("", response_model=PostRead, status_code=201)
def create_posts(
    caption: str = Form(default=""),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return create_post(db, caption, image)


@router.get("/{post_id}", response_model=PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return get_post(db, post_id)


@router.put("/{post_id}", response_model=PostRead)
def edit_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    return update_post(db, post_id, post_data)


@router.delete("/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db)):
    return delete_post(db, post_id)
