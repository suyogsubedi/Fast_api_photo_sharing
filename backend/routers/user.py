from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from routers.schemas import UserBase, UserDisplay
from db import db_user
router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    # Function lai database ko session ra schema deko
    return db_user.create_user(db, request)
