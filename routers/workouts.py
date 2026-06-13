from typing import Annotated

from fastapi import Depends, HTTPException, Path,APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import session, Session
from starlette import status

from database import engine, Base,SessionLocal
from model import Tracker
router=APIRouter()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]

class Workout:
    id:int
    exercise_name:str
    target_muscle:str
    sets:int
    reps:int
    weight_kg:int
    def __init__(self,id,exercise_name,target_muscle,sets,reps,weight_kg):
        self.id=id
        self.exercise_name=exercise_name
        self.target_muscle=target_muscle
        self.sets=sets
        self.reps=reps
        self.weight_kg=weight_kg
class WorkoutRequest(BaseModel):
    exercise_name: str=Field(min_length=3,max_length=20)
    target_muscle: str=Field(min_length=3,max_length=20)
    sets: int=Field(ge=1,le=10)
    reps: int=Field(ge=1)
    weight_kg: int=Field(ge=1)
@router.get("/workouts",status_code=status.HTTP_200_OK)
async def all_workouts(db:db_dependency):
    workout_models= db.query(Tracker).all()
    if workout_models:
        return workout_models
    else:
        raise HTTPException(status_code=404,detail="The table is empty")
@router.post("/workouts/new_workouts/",status_code=status.HTTP_201_CREATED)
async def new_workout(db:db_dependency,newworkout:WorkoutRequest):
    workout_model=Tracker(**newworkout.model_dump())
    db.add(workout_model)
    db.commit()
@router.get("/workouts/workout_by_id/{workout_id}",status_code=status.HTTP_200_OK)
async def workout_by_id(db:db_dependency,workout_id:int):
    workout_model=db.query(Tracker).filter(Tracker.id==workout_id).first()
    if workout_model is not None:
        return workout_model
    else:
        raise HTTPException(status_code=404,detail="Can't find a workout with the given id")
@router.put("/workouts/alter_workouts/{workout_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def alter_workout(db:db_dependency,workout_id:int,workout:WorkoutRequest):
    workout_model=db.query(Tracker).filter(Tracker.id==workout_id).first()
    if workout_model is None:
        raise HTTPException(status_code=404,detail="Can't find a workout with the given id")
    workout_model.target_muscle=workout.target_muscle
    workout_model.sets=workout.sets
    workout_model.reps=workout.reps
    workout_model.weight_kg=workout.weight_kg
    workout_model.exercise_name=workout.exercise_name
    db.add(workout_model)
    db.commit()
@router.delete("/workouts/delete_workout_by_id/{workout_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_by_id(db:db_dependency,workout_id:int=Path(ge=1)):
    workout_model = db.query(Tracker).filter(Tracker.id == workout_id).first()
    if workout_model is None:
        raise HTTPException(status_code=404, detail="Can't find a workout with the given id")
    else:
        db.delete(workout_model)
        db.commit()