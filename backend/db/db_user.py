# This files talks with the database and creates things
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from routers.schemas import UserBase
from .models import DbUser
# For password hashing
from db.hashing import Hash


def create_user(db: Session, request: UserBase):
    """
    Yo Function lai database sanga ko Session chaincha arko schema chaincha
    """
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username==username).first()
    if not user:
        raise HTTPException(
            status_code="404", detail=f"Username with username {username} not found")
    return user
