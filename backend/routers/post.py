import shutil
from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, File
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from routers.schemas import PostBase, PostDisplay, UserAuth
from db.database import get_db
from db import db_post
import random
import string
# Response to getting all the posts is going to be a list
from typing import List
router = APIRouter(
    prefix="/post",
    tags=['post']
)

image_url_types = ['absolute', 'relative']


@router.post("/", response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(
            status_code="405", detail="The image type should be relative or absolute")
    return db_post.create_post(db, request)


@router.get("/", response_model=List[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return db_post.get_all_posts(db)

# Upload image from local computer

@router.post('/image')

def upload_image(image: UploadFile = File(...),current_user: UserAuth = Depends(get_current_user)):
  letters = string.ascii_letters
  rand_str = ''.join(random.choice(letters) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)
  
  return {'filename': path}


@router.get('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete(db, id, current_user.id)

