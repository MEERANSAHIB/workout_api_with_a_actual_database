from sqlalchemy import Column, String, Integer
from database import Base
class Tracker(Base):
    __tablename__='wtracker'
    id=Column(Integer,primary_key=True,index=True)
    exercise_name=Column(String)
    target_muscle=Column(String)
    sets=Column(Integer)
    reps=Column(Integer)
    weight_kg=Column(Integer)

class Users(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    user_name= Column(String)
    hashed_password=Column(String)
    email_id=Column(String)
    first_name=Column(String)
    last_name=Column(String)
    role=Column(String)