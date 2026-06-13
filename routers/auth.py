from typing import Annotated
from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from pydantic import BaseModel, deprecated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal
from model import Users

router=APIRouter()
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]

class new_user_request(BaseModel):
    user_name:str
    password: str
    email_id: str
    first_name:str
    last_name:str
    role:str
def verify_user(user_name,password,db):
    user=db.query(Users).filter(Users.user_name==user_name).first()
    if not user:
        return "This user_name is not present in the database"
    if not bcrypt_context.verify(password,user.hashed_password):
        return "Wrong Combination"
    return user


@router.get("/auth/get_all_users")
async def get_all_users(db:db_dependency):
    user_model=db.query(Users).all()
    return user_model
@router.post("/auth/new_users")
async def new_users(db:db_dependency,new_user:new_user_request):
    user_model=Users(
    user_name=new_user.user_name,
    email_id=new_user.email_id,
    hashed_password=bcrypt_context.hash(new_user.password),
    first_name=new_user.first_name,
    last_name=new_user.last_name,
    role=new_user.role)
    db.add(user_model)
    db.commit()

@router.post("/auth/return_user_details")
async def user_details(new_form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    model=verify_user(new_form.username,new_form.password,db)
    return model

