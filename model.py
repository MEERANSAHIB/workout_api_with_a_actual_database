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

