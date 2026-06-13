from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from model import Users

router=APIRouter()

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
@router.post("/auth/new_users")
async def new_users(db:db_dependency,new_user:new_user_request):
    Users.user_name=new_user.user_name
    Users.email_id=new_user.email_id
    Users.hashed_password=new_user.password
    Users.first_name=new_user.first_name
    Users.last_name=new_user.last_name
    Users.role=new_user.role
    db.add(Users)
    db.commit()
