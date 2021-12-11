from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import Base, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    #hash the password
    hash_password = utils.hash(user.password)
    user.password = hash_password

    my_new_user = models.User(**user.dict())
    db.add(my_new_user)
    db.commit()
    db.refresh(my_new_user)
    return my_new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    return user